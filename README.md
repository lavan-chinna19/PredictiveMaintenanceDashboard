# 🏫 Predictive Maintenance Dashboard for Hostel Facilities

## 📌 Project Overview
This project is a **Business Intelligence (BI) and Machine Learning solution** for managing hostel facilities.  
It predicts device failures, logs complaints, and provides an interactive dashboard for monitoring hostel equipment.  

The goal: **reduce downtime, optimize maintenance, and improve hostel resource management**.

---

## 🛠️ Tech Stack
- **Python** (Pandas, Scikit-learn, Joblib)
- **Streamlit** (interactive dashboard)
- **Plotly** (data visualization)
- **Anaconda + Jupyter Notebooks** (data cleaning, feature engineering, model training)
- **GitHub** (version control & collaboration)

---

## 📂 Project Structure
PredictiveMaintenanceProject/
│
├── app.py # Streamlit app (frontend)
├── predict.py # ML inference helper
├── requirements.txt # Project dependencies
│
├── data/
│ ├── raw/ # Raw CSVs (device inventory, usage logs, maintenance logs)
│ ├── staging/ # Cleaned + feature engineered data
│ └── complaints.csv # User-submitted complaints (ignored in git)
│
├── models/
│ └── rf_model.pkl # Trained Random Forest model
│
├── notebooks/ # Jupyter notebooks
│ ├── 00_setup_environment.ipynb
│ ├── 01_explore_data.ipynb
│ ├── 02_cleaning_and_integration.ipynb
│ ├── 03_feature_engineering.ipynb
│ ├── 04_modeling_and_eval.ipynb
│ ├── 05_streamlit_prep.ipynb
│ └── 06_pbi_prep_and_docs.ipynb
│
└── docs/ # Documentation and PPTs

yaml
Copy code

---

## 🚀 How to Run Locally
### 1️⃣ Setup Environment
```bash
conda create -n hostel_pm python=3.10 -y
conda activate hostel_pm
pip install -r requirements.txt
2️⃣ Run Streamlit App
bash
Copy code
streamlit run app.py
This will open the dashboard in your browser at http://localhost:8501

📊 Features
Overview Page

Total devices

MTBF (Mean Time Between Failures)

Maintenance costs

Failure trends over time

Predictions

Failure probability (Low/Medium/High risk)

Risk distribution histograms

Download risky devices as CSV

Device Details

Historical usage and prediction history for each device

Complaints

Submit complaints per device

View complaint logs

Run Model

Trigger predictions and update results

✅ Completed Work
Data cleaning & integration

Feature engineering

Model training (Random Forest)

Prediction pipeline (predict.py)

Interactive dashboard (app.py)

🔜 Future Work
Add alerting system (email/SMS for high-risk devices)

Deploy dashboard on Streamlit Cloud for public access

Integrate with real-time IoT sensor data

👨‍💻 Team Roles
Backend (Data pipeline & DB) – integrates and cleans hostel datasets

Machine Learning – builds predictive model and risk scores

Frontend (Streamlit Dashboard) – builds interactive BI dashboard

📷 Screenshots (to add)
(Insert screenshots of your dashboard pages here for presentation)

📑 License
This project is for academic purposes and internal demonstration only.

yaml
Copy code

---

## ✅ Next steps for you
1. Save this as `README.md` in your project folder.  
2. Stage & commit:
   ```powershell
   git add README.md
   git commit -m "docs: add project README"
   git push origin main
