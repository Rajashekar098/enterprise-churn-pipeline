import pandas as pd
import numpy as np

print("Loading base dataset...")
base_df = pd.read_csv('raw_churn_data.csv')

# 1. Clean data type anomalies in TotalCharges
base_df['TotalCharges'] = pd.to_numeric(base_df['TotalCharges'].str.strip(), errors='coerce')
base_df['TotalCharges'] = base_df['TotalCharges'].fillna(0.0)

# 2. Scale dataset to 100,000+ records to simulate enterprise volume
target_rows = 105645  # Exactly 15x multiplier
multiplier = int(np.ceil(target_rows / len(base_df)))

print(f"Synthesizing enterprise volume ({target_rows:,} records)...")
dfs = []
for i in range(multiplier):
    temp = base_df.copy()
    temp['customerID'] = temp['customerID'] + f"_{i:02d}"
    # Introduce controlled micro-variance in financial metrics
    variance = np.random.uniform(0.97, 1.03, size=len(temp))
    temp['MonthlyCharges'] = (temp['MonthlyCharges'] * variance).round(2)
    temp['TotalCharges'] = (temp['TotalCharges'] * variance).round(2)
    dfs.append(temp)

large_df = pd.concat(dfs, ignore_index=True).iloc[:target_rows]

# 3. Vectorized Feature Engineering
print("Engineering retention risk metrics...")

# Binary churn flag
large_df['Churn_Flag'] = (large_df['Churn'] == 'Yes').astype(int)

# Customer Lifetime Value (LTV) Proxy
large_df['Estimated_LTV'] = (large_df['MonthlyCharges'] * large_df['tenure']).round(2)

# Tenure Segment Classification
conditions = [
    (large_df['tenure'] <= 12),
    (large_df['tenure'] > 12) & (large_df['tenure'] <= 36),
    (large_df['tenure'] > 36)
]
choices = ['New Account (<= 1yr)', 'Established (1-3yrs)', 'Loyal (> 3yrs)']
large_df['Tenure_Cohort'] = np.select(conditions, choices, default='Unknown')

# Risk Scoring: month-to-month contracts + high monthly charges = elevated risk
large_df['High_Risk_Flag'] = np.where(
    (large_df['Contract'] == 'Month-to-month') & (large_df['MonthlyCharges'] >= 70.0),
    1,
    0
)

# 4. Generate Executive KPI Aggregations (Optimized for Tableau)
print("Computing executive summary aggregation...")
summary_df = large_df.groupby(['Contract', 'InternetService', 'PaymentMethod', 'Tenure_Cohort']).agg(
    Total_Customers=('customerID', 'count'),
    Total_Churned=('Churn_Flag', 'sum'),
    Avg_Monthly_Charges=('MonthlyCharges', 'mean'),
    Total_Revenue=('TotalCharges', 'sum'),
    High_Risk_Count=('High_Risk_Flag', 'sum')
).reset_index()

summary_df['Churn_Rate'] = (summary_df['Total_Churned'] / summary_df['Total_Customers']).round(4)
summary_df['Avg_Monthly_Charges'] = summary_df['Avg_Monthly_Charges'].round(2)
summary_df['Total_Revenue'] = summary_df['Total_Revenue'].round(2)

# 5. Export Datasets
print("Exporting production assets...")
large_df.to_csv('Enterprise_Churn_100k.csv', index=False)
summary_df.to_csv('Tableau_Executive_Summary.csv', index=False)

print("\n--- Pipeline Execution Complete ---")
print(f"Full Dataset exported: 'Enterprise_Churn_100k.csv' ({len(large_df):,} rows)")
print(f"Executive Aggregation exported: 'Tableau_Executive_Summary.csv' ({len(summary_df):,} rows)")
