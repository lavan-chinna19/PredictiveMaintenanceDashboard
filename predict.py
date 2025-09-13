# predict.py
import joblib
import pandas as pd
from pathlib import Path

BASE = Path(r"C:\Users\lavan\OneDrive\Desktop\PredictiveMaintenanceProject")
ST = BASE / "data" / "staging"
MODEL_PATH = BASE / "models" / "rf_model.pkl"

def load_model(path=MODEL_PATH):
    return joblib.load(path)

def compute_predictions(features_df, model=None):
    """
    features_df: DataFrame containing required columns:
      HoursUsed, Hours_7d_mean, Temperature, Vibration, DaysSinceLastMaint
    Returns features_df with added columns 'pred_prob' and 'priority'
    """
    if model is None:
        model = load_model()
    X = features_df[["HoursUsed","Hours_7d_mean","Temperature","Vibration","DaysSinceLastMaint"]].fillna(0)
    probs = model.predict_proba(X)[:,1]
    features_df = features_df.copy()
    features_df["pred_prob"] = probs
    features_df["priority"] = features_df["pred_prob"] * (1 + features_df["DaysSinceLastMaint"]/365.0)
    return features_df

def write_latest_predictions(features_df, out_path=ST/"predictions_latest.csv"):
    # keep latest row per device
    feat = features_df.sort_values(["DeviceID","Date"])
    latest = feat.groupby("DeviceID").tail(1)
    latest[["DeviceID","Date","pred_prob","priority"]].to_csv(out_path, index=False)
    return out_path

if __name__ == "__main__":
    # Quick local run
    feat = pd.read_csv(ST/"features_for_model.csv", parse_dates=["Date"])
    model = load_model()
    pred_df = compute_predictions(feat, model=model)
    out = write_latest_predictions(pred_df)
    print("Wrote predictions to:", out)
