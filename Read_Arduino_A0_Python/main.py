import serial
import time

# Replace 'YOUR_ARDUINO_PORT' with the appropriate serial port
# e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux.
arduino_port = 'COM3'
reference_voltage = 5.0  # Reference voltage in volts

# Establish serial communication with Arduino
ser = serial.Serial(arduino_port, 9600, timeout=1)

try:
    while True:
        # Read data from Arduino
        line = ser.readline().decode().strip()

        if line:
            try:
                analog_value = int(line)
                voltage = (analog_value / 1023.0) * reference_voltage
                print(f"Analog Value (A0): {analog_value}, Voltage: {voltage:.2f} V")
            except ValueError:
                print("Invalid data received from Arduino.")

except KeyboardInterrupt:
    # Close the serial connection and exit when the user presses Ctrl+C
    ser.close()
    print("\nExiting...")
