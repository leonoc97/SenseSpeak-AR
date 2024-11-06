import serial
import csv
import threading


def read_serial(ser, output_file, start_event):
    """Read data from the serial port and save between STF and EOF markers."""
    capture_data = False
    data_lines = []

    # Wait until the start event is triggered
    start_event.wait()
    print("Starting data capture from ESP...")
    line = ser.readline().decode('utf-8').strip()
    print(line)

    while True:
        line = ser.readline().decode('utf-8').strip()

        # Check for start and end markers
        if line == "STF":
            capture_data = True
            data_lines = []  # Clear any previous data
            print("Start of data capture detected.")
        elif line == "EOF":
            print("End of data capture detected. Writing to CSV...")
            with open(output_file, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for data_line in data_lines:
                    writer.writerow(data_line.split(";"))
            print(f"Data saved to {output_file}")
            capture_data = False
        elif capture_data:
            # Collect lines between STF and EOF
            data_lines.append(line)
        else:
            # Print any other messages received from ESP
            print(f"Received from ESP: {line}")


def send_commands(ser, start_event):
    """Send commands to the ESP based on user keyboard input and start reading on first input."""
    started_reading = False

    while True:
        command = input("Press any key to start reading or enter a command to send to ESP (type 'exit' to quit): ")

        # Start reading on the first input
        if not started_reading:
            start_event.set()  # Trigger the reading thread to start
            started_reading = True
            print("Reading started on first input.")

        if command.lower() == "exit":
            print("Exiting command sender...")
            break

        # Send command to ESP
        ser.write((command + '\n').encode('utf-8'))
        print(f"Sent to ESP: {command}")


def read_serial_to_csv_with_commands(port, baudrate=9600, timeout=1, output_file="sensor_data.csv"):
    # Configure the serial connection
    ser = serial.Serial(port, baudrate, timeout=timeout)

    # Event to start the reading process
    start_event = threading.Event()

    try:
        # Start the reading thread with the start event
        reader_thread = threading.Thread(target=read_serial, args=(ser, output_file, start_event))
        reader_thread.daemon = True
        reader_thread.start()

        # Start sending commands in the main thread
        send_commands(ser, start_event)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Close the serial port
        ser.close()
        print("Serial port closed.")


# Example usage
read_serial_to_csv_with_commands(port='COM16', baudrate=115200, output_file='sensor_data.csv')
