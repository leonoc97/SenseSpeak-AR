import serial
import csv

# Replace with your actual serial port and baud rate
SERIAL_PORT = 'COM3'       # e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux/macOS
BAUD_RATE = 115200

# CSV file to save sensor data
CSV_FILENAME = 'mpu6050_data.csv'

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
            headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
            csv_writer.writerow(headers)

            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    # Split the line into data values
                    data_values = line.split(',')

                    if len(data_values) == 6:
                        # Convert string values to integers or floats
                        try:
                            sensor_data = [float(value.strip()) for value in data_values]

                            # Write sensor data to CSV file
                            csv_writer.writerow(sensor_data)
                            csv_file.flush()  # Ensure data is written to disk

                            # Optionally, print the sensor data
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
