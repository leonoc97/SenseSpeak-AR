import csv
import random

# Number of entries
num_entries = 500

# File to save the generated data
output_file = "synthetic_sensor_data.csv"

# Headers for the CSV
headers = [
    "t", "X_0", "Y_0", "Z_0",
    "X_1", "Y_1", "Z_1",
    "X_2", "Y_2", "Z_2",
    "X_3", "Y_3", "Z_3",
    "X_4", "Y_4", "Z_4"
]

# Generate synthetic data
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    # Write headers
    writer.writerow(headers)

    # Generate entries
    for t in range(num_entries):
        # Random values for each axis, simulating sensor readings
        row = [t] + [random.randint(-300, 300) for _ in range(15)]
        writer.writerow(row)

print(f"Synthetic data with {num_entries} entries has been saved to {output_file}")
