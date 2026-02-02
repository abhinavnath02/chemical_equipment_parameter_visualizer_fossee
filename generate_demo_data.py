import pandas as pd
import numpy as np

def generate_normal_data(filename="demo_1_normal_operation.csv", count=50):
    """
    Generates data within safe operating limits.
    Demonstrates: parameter distribution, basic charts, standard summary stats.
    """
    types = ['Pump', 'Heat Exchanger', 'Reactor', 'Tank', 'Compressor']
    data = {
        'Equipment Name': [f'EQ-{i:03d}' for i in range(1, count + 1)],
        'Type': np.random.choice(types, count),
        'Flowrate': np.random.uniform(100, 450, count).round(1),    # Safe: 50-500
        'Pressure': np.random.uniform(200, 700, count).round(1),    # Safe: 100-800
        'Temperature': np.random.uniform(100, 300, count).round(1)  # Safe: 50-350
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created {filename}")

def generate_critical_data(filename="demo_2_safety_alerts.csv", count=30):
    """
    Generates data exceeding critical thresholds.
    Demonstrates: Safety Status Chart (Red/Amber), Critical Warning List.
    Thresholds: Flow > 600, Pressure > 1000, Temp > 400
    """
    types = ['Reactor', 'Compressor']
    data = {
        'Equipment Name': [f'CRIT-{i:03d}' for i in range(1, count + 1)],
        'Type': np.random.choice(types, count),
        'Flowrate': np.random.uniform(550, 750, count).round(1),    # Mix of Warning/Critical
        'Pressure': np.random.uniform(900, 1200, count).round(1),   # Mostly Critical
        'Temperature': np.random.uniform(380, 450, count).round(1)  # High Heat
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created {filename}")

def generate_correlated_data(filename="demo_3_smart_correlations.csv", count=100):
    """
    Generates data with strong linear relationships.
    Demonstrates: 'Smart Insights' - Correlations.
    Formula: Pressure = 2 * Temperature + noise
    """
    types = ['Heat Exchanger']
    temps = np.linspace(100, 300, count)
    # Add small random noise to make it realistic but still highly correlated
    pressures = (temps * 2.5) + np.random.normal(0, 10, count)
    
    data = {
        'Equipment Name': [f'HE-{i:03d}' for i in range(1, count + 1)],
        'Type': ['Heat Exchanger'] * count,
        'Flowrate': np.random.uniform(200, 300, count).round(1),
        'Pressure': pressures.round(1),
        'Temperature': temps.round(1)
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created {filename}")

def generate_outlier_data(filename="demo_4_statistical_anomalies.csv", count=50):
    """
    Generates mostly uniform data with 2 significant statistical outliers.
    Demonstrates: 'Smart Insights' - Statistical Deviations (Z-Score).
    """
    types = ['Pump']
    # Create very consistent data (low standard deviation)
    flowrates = np.random.normal(200, 5, count) # Mean 200, SD 5
    pressures = np.random.normal(400, 10, count)
    temps = np.random.normal(150, 5, count)
    
    # Introduce outliers (far away from mean)
    # Outlier 1: Massive Flowrate
    flowrates[-1] = 600 # 80 SDs away! (but just on the edge of "Critical" max 600)
    
    # Outlier 2: Very Low Pressure (but still positive)
    pressures[-2] = 50 
    
    data = {
        'Equipment Name': [f'PUMP-{i:03d}' for i in range(1, count + 1)],
        'Type': ['Pump'] * count,
        'Flowrate': flowrates.round(1),
        'Pressure': pressures.round(1),
        'Temperature': temps.round(1)
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created {filename}")

if __name__ == "__main__":
    generate_normal_data()
    generate_critical_data()
    generate_correlated_data()
    generate_outlier_data()
