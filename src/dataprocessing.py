import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def load_data(file_path: str):

    df = pd.read_csv(file_path)
    df = df.rename(columns={
        'Type': 'machine_type',
        'Air temperature [K]': 'air_temperature',
        'Process temperature [K]': 'process_temperature',
        'Rotational speed [rpm]': 'rotational_speed',
        'Torque [Nm]': 'torque',
        'Tool wear [min]': 'tool_wear',
        'Machine failure': 'target'
    })
    df = df.drop(columns=['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'], errors='ignore')
    df = pd.get_dummies(df, columns=['machine_type'], prefix = 'machine_type', dtype=int)
    df['power_watts'] = df['torque']*df['rotational_speed']
    df['temp_delta'] = df['process_temperature'] - df['air_temperature']
    df['overstrain_factor'] = df['tool_wear']*df['torque']
    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, stratify =y, random_state = 42)

    return X_train, X_test, y_train, y_test

if __name__ == 'main':
    load_data('data/ai4i2020.csv')