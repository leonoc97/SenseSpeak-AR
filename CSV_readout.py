import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np


def plot_sensor_data(csv_file):
    # Initialize an empty list to store rows
    rows = []

    # Read the CSV file with manual parsing to handle row length inconsistencies
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            # Adjust for expected column count based on the file format
            if len(row) == 18:  # Adjust this count based on expected structure
                rows.append(row)
            else:
                rows.append(row + [''] * (18 - len(row)))

    # Convert to a DataFrame
    data = pd.DataFrame(rows)

    # Drop any non-numeric header rows and reset index
    data = data.dropna().reset_index(drop=True)

    # Convert all columns to numeric, setting errors to NaN for invalid entries
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Define sensor and axis names
    sensor_names = [f'Sensor_{i}' for i in range(5)]
    axis_labels = ['X', 'Y', 'Z']

    # Extract and label sensor columns
    sensors_data = {f'{sensor}_{axis}': data.iloc[:, i + 1]
                    for i, (sensor, axis) in enumerate([(s, a) for s in sensor_names for a in axis_labels])}
    sensor_df = pd.DataFrame(sensors_data)

    # Check which sensors have active data by looking for non-zero or non-NaN values
    active_sensors = {}
    for sensor in sensor_names:
        # Check if any data is non-zero or non-NaN for this sensor across all axes
        active_data = (sensor_df[f"{sensor}_X"].replace(0, np.nan).notna() |
                       sensor_df[f"{sensor}_Y"].replace(0, np.nan).notna() |
                       sensor_df[f"{sensor}_Z"].replace(0, np.nan).notna())

        if active_data.any():  # If there's any valid data for this sensor
            active_sensors[sensor] = True

    # Plot data for each active sensor
    for sensor in active_sensors:
        plt.figure(figsize=(10, 6))
        plt.title(f"{sensor} Axis Data Over Time")

        for axis in axis_labels:
            plt.plot(sensor_df[f"{sensor}_{axis}"], label=f"{axis} Axis")

        plt.xlabel("Time (or index)")
        plt.ylabel("Sensor Values")
        plt.legend()
        plt.grid(True)
        plt.show()


def plot_all_sensors_in_one(csv_file):
    # Manually specify the correct headers
    headers = [
        "t", "X_0", "Y_0", "Z_0",
        "X_1", "Y_1", "Z_1",
        "X_2", "Y_2", "Z_2",
        "X_3", "Y_3", "Z_3",
        "X_4", "Y_4", "Z_4"
    ]

    # Read the CSV file with the corrected headers
    data = pd.read_csv(csv_file, delimiter=';', header=None, names=headers, skiprows=1)

    # Define sensor names and axis labels
    sensor_names = [f'Sensor_{i}' for i in range(5)]
    axis_labels = ['X', 'Y', 'Z']

    # Create a dictionary to store data for each sensor axis
    sensors_data = {f'{sensor}_{axis}': data[f"{axis}_{i}"]
                    for i, sensor in enumerate(sensor_names) for axis in axis_labels}

    # Convert to a DataFrame for easier manipulation
    sensor_df = pd.DataFrame(sensors_data)

    # Plot all sensors in one plot
    plt.figure(figsize=(14, 8))
    plt.title("All Sensors Axis Data Over Time")

    # Different colors for each sensor-axis combination
    for sensor in sensor_names:
        for axis in axis_labels:
            plt.plot(sensor_df[f"{sensor}_{axis}"], label=f"{sensor} {axis} Axis")

    plt.xlabel("Time (or index)")
    plt.ylabel("Sensor Values")
    plt.legend()
    plt.grid(True)
    plt.show()
# Example usage:
plot_sensor_data("synthetic_sensor_data.csv")
#plot_all_sensors_in_one("sensor_data.csv")
