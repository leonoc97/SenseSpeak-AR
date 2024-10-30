import serial
import csv

SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

# CSV file to save sensor data
CSV_FILENAME = 'sensor_data.csv'

def main():
    try:
        # Open serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        # Open CSV file for writing
        with open(CSV_FILENAME, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            print(f"Saving data to {CSV_FILENAME}")

            # Write header row to CSV
            headers = []
            for sensor_num in range(1, 6):  # Sensors 1 to 5
                headers.append(f"Sensor {sensor_num} X")
                headers.append(f"Sensor {sensor_num} Y")
                headers.append(f"Sensor {sensor_num} Z")
            csv_writer.writerow(headers)

            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    # Split the line into data values
                    data_values = line.split(',')

                    if len(data_values) == 15:
                        # Convert string values to integers or floats
                        try:
                            sensor_data = [float(value.strip()) for value in data_values]

                            # Write sensor data to CSV file
                            csv_writer.writerow(sensor_data)
                            csv_file.flush()  # Ensure data is written to disk

                            # Optional for debugging
                            print(sensor_data)
                        except ValueError as e:
                            print(f"ValueError: {e} in line: {line}")
                    else:
                        # Handle unexpected data format
                        print(f"Unexpected data format: {line}")
                else:
                    # No data received, wait briefly
                    pass

    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == '__main__':
    main()
