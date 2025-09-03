# 🛠️ Predictive Maintenance Dashboard for Hostel Facilities

## 📌 Project Overview
This project focuses on building a **Predictive Maintenance System** for hostel facilities (e.g., ACs, washing machines, water heaters, pumps).  
The goal is to **predict equipment failures before they happen** and provide a **Business Intelligence (BI) dashboard** for hostel administrators to make proactive decisions.  

By combining **data analysis**, **machine learning**, and **Power BI visualizations**, this project improves:
- ✅ Reduced equipment downtime  
- ✅ Lower maintenance costs  
- ✅ Improved student comfort and safety  

---

## 📂 Project Structure
PredictiveMaintenanceProject/
│
├── data/
│ ├── raw/ # Original data (ignored in GitHub)
│ └── staging/ # Cleaned/processed data for analysis & BI
│
├── notebooks/ # Jupyter notebooks (step by step workflow)
│ ├── 00_setup_environment.ipynb
│ ├── 01_explore_profile.ipynb
│ ├── 02_clean_etl.ipynb
│ ├── 03_feature_engineering.ipynb
│ ├── 04_modeling_and_eval.ipynb
│ ├── 05_generate_predictions.ipynb
│ └── 06_pbi_prep_and_docs.ipynb
│
├── models/ # Trained ML models (e.g., Random Forest)
├── docs/ # Documentation & reports
├── .gitignore # Ignore raw data, checkpoints, cache
└── README.md # Project overview (this file)

---

## ⚙️ Tech Stack
- **Language:** Python (Anaconda / Jupyter Notebook)  
- **Libraries:** Pandas, Scikit-learn, Matplotlib, Seaborn, Joblib  
- **Dashboard:** Power BI (CSV integration from staging)  
- **Version Control:** Git & GitHub  

---

## 📊 Workflow

### 🔹 Phase 0 — Project Kickoff
- Define scope, stakeholders, KPIs (MTBF, MTTR, predicted failures).
- Tools chosen: Jupyter Notebook (Python), Power BI.

### 🔹 Phase 1 — Get Data
- Datasets:  
  - `hostel_device_inventory_small.csv`  
  - `hostel_usage_logs_small.csv`  
  - `hostel_maintenance_logs_small.csv`  
- Stored in `data/raw/`.

### 🔹 Phase 2 — Clean & ETL
- Standardized Device IDs, dates, failure flags.  
- Removed duplicates, handled missing values.  
- Saved cleaned files to `data/staging/`.

### 🔹 Phase 3 — Feature Engineering
- Rolling averages of usage (7 days).  
- Days since last maintenance.  
- Labels for predicting failures in next 7 days.

### 🔹 Phase 4 — Modeling & Evaluation
- Trained a **Random Forest Classifier**.  
- Evaluated using Precision, Recall, F1-score, ROC-AUC.  

### 🔹 Phase 5 — Predictions
- Generated risk scores (`pred_prob`) for each device.  
- Created `predictions_latest.csv` for BI dashboard.

### 🔹 Phase 6 — Power BI Integration
- Fact & Dimension tables prepared (`fact_usage.csv`, `dim_device.csv`).  
- Built BI Dashboard with KPIs, trends, and prediction tables.  

---

## 📈 KPIs in Dashboard
- **MTBF (Mean Time Between Failures)**  
- **MTTR (Mean Time To Repair)**  
- **Predicted Failure Probability per Device**  
- **Maintenance Priority Score**  

---

## 🚀 How to Run
1. Clone this repo:
   ```bash
   git clone https://github.com/lavan-chinna19/PredictiveMaintenanceDashboard.git
