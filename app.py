# app.py
# Streamlit app for Hostel Predictive Maintenance

import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from predict import load_model, compute_predictions, write_latest_predictions

# -------------------------
# Config / Paths
# -------------------------
BASE = Path(r"C:\Users\lavan\OneDrive\Desktop\PredictiveMaintenanceProject")
STAGING = BASE / "data" / "staging"
MODELS = BASE / "models"
COMPLAINTS_CSV = BASE / "data" / "complaints.csv"

# -------------------------
# Cached loaders
# -------------------------
@st.cache_data
def load_devices():
    p = STAGING / "dim_device.csv"
    if not p.exists():
        p = STAGING / "hostel_device_inventory_clean.csv"
    return pd.read_csv(p)

@st.cache_data
def load_usage():
    p = STAGING / "fact_usage.csv"
    if not p.exists():
        p = STAGING / "hostel_usage_logs_clean.csv"
    return pd.read_csv(p, parse_dates=["Date"])

@st.cache_data
def load_predictions():
    p = STAGING / "predictions_latest.csv"
    if p.exists():
        return pd.read_csv(p, parse_dates=["Date"])
    # fallback: compute if features exist
    feat_p = STAGING / "features_for_model.csv"
    if feat_p.exists():
        feat = pd.read_csv(feat_p, parse_dates=["Date"])
        model = load_model()
        pred_df = compute_predictions(feat, model)
        write_latest_predictions(pred_df)
        return pd.read_csv(p, parse_dates=["Date"])
    return pd.DataFrame(columns=["DeviceID","Date","pred_prob","priority"])

def load_complaints():
    if COMPLAINTS_CSV.exists() and COMPLAINTS_CSV.stat().st_size > 0:
        try:
            return pd.read_csv(COMPLAINTS_CSV, parse_dates=["Datetime"])
        except ValueError:
            # If file exists but no header / wrong format → reload as no header
            df = pd.read_csv(COMPLAINTS_CSV, header=None)
            if df.shape[1] == 4:  # expect 4 cols
                df.columns = ["DeviceID","Description","ReportedBy","Datetime"]
                df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
                return df
            else:
                return pd.DataFrame(columns=["DeviceID","Description","ReportedBy","Datetime"])
    else:
        return pd.DataFrame(columns=["DeviceID","Description","ReportedBy","Datetime"])


def log_complaint(device_id, desc, reporter):
    import csv, datetime
    COMPLAINTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLAINTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([device_id, desc, reporter, datetime.datetime.now().isoformat()])
    st.success("Complaint logged!")

# -------------------------
# UI Layout
# -------------------------
st.set_page_config(layout="wide", page_title="Hostel Predictive Maintenance")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview","Predictions","Device Details","Complaints","Run Model"])

# Load data
devices = load_devices()
usage = load_usage()
preds = load_predictions()
complaints = load_complaints()

# -------------------------
# Overview page
# -------------------------
if page == "Overview":
    st.title("🏫 Hostel Predictive Maintenance - Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total devices", int(devices.shape[0]) if not devices.empty else 0)

    high_risk = int((preds['pred_prob'] > 0.7).sum()) if not preds.empty else 0
    col2.metric("High risk devices (p>0.7)", high_risk)

    if "HoursUsed" in usage.columns and "FailureFlag" in usage.columns:
        total_hours = usage["HoursUsed"].sum()
        failures = usage["FailureFlag"].sum()
        mtbf = total_hours / failures if failures > 0 else None
        col3.metric("MTBF (hours)", f"{mtbf:.1f}" if mtbf else "N/A")
    else:
        col3.metric("MTBF (hours)", "N/A")

    if "Cost" in usage.columns:
        col4.metric("Maintenance cost (sum)", f"{usage['Cost'].sum():.2f}")
    else:
        col4.metric("Maintenance cost (sum)", "N/A")

    st.markdown("### Failures over time")
    if "Date" in usage.columns and "FailureFlag" in usage.columns:
        agg = usage.groupby("Date")["FailureFlag"].sum().reset_index()
        fig = px.line(agg, x="Date", y="FailureFlag", title="Failures over time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Usage or FailureFlag data not available for time-series")

# -------------------------
# Predictions page
# -------------------------
elif page == "Predictions":
    st.title("🔮 Predicted Failure Risks")
    if preds.empty:
        st.info("No predictions found. Use 'Run Model' to compute predictions.")
    else:
        th = st.slider("High risk threshold (probability)", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        table = preds.merge(devices, on="DeviceID", how="left")
        table["RiskLevel"] = pd.cut(table["pred_prob"], bins=[-0.01, th, 0.99, 1.0], labels=["Low", "Medium", "High"])
        st.markdown("### Top risky devices")
        st.dataframe(
            table.sort_values("pred_prob", ascending=False)[
                ["DeviceID","DeviceType","Location","pred_prob","priority","RiskLevel"]
            ].head(200),
            use_container_width=True
        )
        st.markdown("### Risk distribution")
        fig = px.histogram(table, x="pred_prob", nbins=20, title="Prediction probability distribution")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Device Details
# -------------------------
elif page == "Device Details":
    st.title("🔍 Device Details & History")
    if devices.empty:
        st.info("No device inventory data available.")
    else:
        sel = st.selectbox("Select Device", devices["DeviceID"].unique())
        d_usage = usage[usage["DeviceID"]==sel].sort_values("Date")
        d_pred = preds[preds["DeviceID"]==sel].sort_values("Date", ascending=False)

        st.subheader("Usage history")
        if not d_usage.empty:
            fig = px.line(d_usage, x="Date", y="HoursUsed", title=f"Hours used for {sel}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No usage history available for this device")

        st.subheader("Prediction history")
        if not d_pred.empty:
            st.table(d_pred[["Date","pred_prob","priority"]].head(10))
        else:
            st.info("No predictions available for this device")

# -------------------------
# Complaints page
# -------------------------
elif page == "Complaints":
    st.title("📩 Complaints")
    with st.form("complaint_form"):
        if not devices.empty:
            d = st.selectbox("Device", devices["DeviceID"].unique())
        else:
            d = st.text_input("Device ID (no inventory loaded)")
        reporter = st.text_input("Reported by")
        desc = st.text_area("Description")
        submitted = st.form_submit_button("Submit")
        if submitted:
            log_complaint(d, desc, reporter)
            st.rerun()   # fixed here

    st.markdown("### Complaint log")
    if not complaints.empty:
        st.dataframe(complaints.sort_values("Datetime", ascending=False), use_container_width=True)
    else:
        st.info("No complaints logged yet.")

# -------------------------
# Run Model page
# -------------------------
elif page == "Run Model":
    st.title("⚙️ Run prediction pipeline")
    st.markdown("Compute predictions from features and save to staging.")
    if st.button("Run predictions now"):
        feat_p = STAGING / "features_for_model.csv"
        if not feat_p.exists():
            st.error("features_for_model.csv not found in staging.")
        else:
            feat = pd.read_csv(feat_p, parse_dates=["Date"])
            model = load_model()
            pred_df = compute_predictions(feat, model)
            out = write_latest_predictions(pred_df)
            st.success(f"Predictions updated: {out}")
            st.rerun()   # fixed here
