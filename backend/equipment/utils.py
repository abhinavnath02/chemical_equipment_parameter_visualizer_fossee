import pandas as pd

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

    summary = {
        "total_equipment": len(df),
        "avg_flowrate": df['Flowrate'].mean(),
        "avg_pressure": df['Pressure'].mean(),
        "avg_temperature": df['Temperature'].mean(),
        "type_distribution": df['Type'].value_counts().to_dict()
    }

    return summary
