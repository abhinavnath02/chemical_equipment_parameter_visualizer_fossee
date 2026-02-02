import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature'
]

def analyze_csv(file):
    df = pd.read_csv(file)

    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        raise ValueError("Invalid CSV format")

    # Equipment by type distribution
    equipment_by_type = df['Type'].value_counts().to_dict()
    
    # Individual equipment data
    equipment_data = []
    for _, row in df.iterrows():
        equipment_data.append({
            'name': row['Equipment Name'],
            'type': row['Type'],
            'flowrate': float(row['Flowrate']),
            'pressure': float(row['Pressure']),
            'temperature': float(row['Temperature'])
        })

    # --- Smart Insights (Correlations & Outliers) ---
    
    # 1. Correlations
    # Select only numeric columns for correlation
    numeric_df = df[['Flowrate', 'Pressure', 'Temperature']]
    corr_matrix = numeric_df.corr()
    
    correlations = []
    for col1 in numeric_df.columns:
        for col2 in numeric_df.columns:
            if col1 >= col2: continue  # Avoid duplicates (A-B vs B-A) or self-correlation
            
            val = corr_matrix.loc[col1, col2]
            if abs(val) > 0.5:  # Threshold for "significant"
                correlations.append({
                    "pair": f"{col1} & {col2}",
                    "value": round(val, 2),
                    "interpretation": "Strong Positive" if val > 0.7 else "Strong Negative" if val < -0.7 else "Moderate"
                })

    # 2. Outliers (Z-Score > 2)
    outliers = []
    for col in numeric_df.columns:
        stats = numeric_df[col].describe()
        mean = stats['mean']
        std = stats['std']
        
        if std == 0: continue

        # Identify rows where |z| > 2
        for idx, val in numeric_df[col].items():
            z_score = (val - mean) / std
            if abs(z_score) > 2:
                outliers.append({
                    "equipment": df.loc[idx, 'Equipment Name'],
                    "parameter": col,
                    "value": float(val),
                    "mean": round(mean, 1),
                    "deviation": f"{round(z_score, 1)}σ"
                })
    
    summary = {
        "total_equipment": len(df),
        "avg_flowrate": float(df['Flowrate'].mean()),
        "avg_pressure": float(df['Pressure'].mean()),
        "avg_temperature": float(df['Temperature'].mean()),
        "equipment_by_type": equipment_by_type,
        "equipment_data": equipment_data,
        "smart_insights": {
            "correlations": correlations,
            "outliers": outliers[:10]  # Cap at 10 to keep JSON small
        }
    }

    return summary
