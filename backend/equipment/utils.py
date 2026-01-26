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

    summary = {
        "total_equipment": len(df),
        "avg_flowrate": float(df['Flowrate'].mean()),
        "avg_pressure": float(df['Pressure'].mean()),
        "avg_temperature": float(df['Temperature'].mean()),
        "equipment_by_type": equipment_by_type,
        "equipment_data": equipment_data
    }

    return summary
