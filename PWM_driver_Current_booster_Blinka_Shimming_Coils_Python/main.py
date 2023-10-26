#
# The program with GUI to control the electronic driver for the shimming coils (four channels).
# PWM driver with the current booster.
# Connect Blinka USB-I2C adapter to PC.
#
# Yujie Zhao, University of St. Andrews, Scotland, 30.07.2023
#

import os
import busio
import board
import adafruit_pca9685
import tkinter as tk
from tkinter import ttk
import logging

# Set BLINKA_MCP2221 environment variable to enable MCP2221 support
os.environ['BLINKA_MCP2221'] = '1'

# Create the I2C bus interface.
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Specify the PCA9685 address (0x40) when creating the instance.
pca = adafruit_pca9685.PCA9685(i2c_bus, address=0x40)

# Set the default frequency to 1500 Hz
pca.frequency = 1500

# Function to update the duty cycle for a channel based on the user input
def update_duty_cycle(channel):
    try:
        duty_cycle = float(duty_entries[channel - 1].get())
        pca.channels[channel - 1].duty_cycle = int(duty_cycle * 0xFFFF)  # Convert to 16-bit value

        # Log the duty cycle change
        logging.info(f"Channel {channel} duty cycle set to {duty_cycle}")

        # Write the new value to the log file
        with open('duty_cycle.log', 'a') as log_file:
            log_file.write(f"Channel {channel} duty cycle set to {duty_cycle}\n")

    except ValueError:
        pass  # If the user enters an invalid value, ignore it

# Function to update the PWM frequency based on the user input
def update_pwm_frequency():
    try:
        frequency = float(freq_entry.get())

        # Write the PWM frequency change to the log file
        logging.info(f"PWM frequency set to {frequency:.2f} Hz")

        # Set the new PWM frequency directly to the PCA9685 instance
        pca.frequency = frequency

        # Write the new value to the log file with up to two decimal places
        with open('duty_cycle.log', 'a') as log_file:
            log_file.write(f"PWM frequency set to {frequency:.2f} Hz\n")

    except ValueError:
        pass  # If the user enters an invalid value, ignore it

# Function to apply the updated duty cycles and PWM frequency to PCA9685
def apply_settings():
    update_pwm_frequency()
    for channel in range(1, 17):
        update_duty_cycle(channel)

    # Fully rewrite the log file with the new values
    with open('duty_cycle.log', 'w') as log_file:
        log_file.write(f"PWM frequency set to {pca.frequency:.2f} Hz\n")
        for channel in range(1, 17):
            duty_cycle = pca.channels[channel - 1].duty_cycle / 0xFFFF
            log_file.write(f"Channel {channel} duty cycle set to {duty_cycle:.2f}\n")

    # Read default values from the log file (if it exists)
    read_default_values()

# Function to stop the program
def stop_program():
    root.quit()

# Function to read default values from the log file
def read_default_values():
    if os.path.exists('duty_cycle.log'):
        with open('duty_cycle.log', 'r') as log_file:
            lines = log_file.readlines()
            for line in lines:
                if "duty cycle" in line:
                    channel = int(line.split()[1])
                    duty_cycle = float(line.split()[-1])
                    duty_entries[channel - 1].delete(0, tk.END)
                    duty_entries[channel - 1].insert(0, str(duty_cycle))
                elif "PWM frequency" in line and not freq_entry.get():
                    frequency = float(line.split()[-2])
                    freq_entry.delete(0, tk.END)
                    freq_entry.insert(0, f"{frequency:.2f}")

# GUI setup
root = tk.Tk()
root.title("PCA9685 PWM Control")

# Label for the duty cycle explanation
ttk.Label(root, text="Duty cycle ratio (0-1)").grid(row=0, column=0, columnspan=2)

# Labels and Entry widgets for duty cycles
duty_entries = []
for channel in range(1, 17):
    ttk.Label(root, text=f"Channel {channel}:").grid(row=channel, column=0)
    entry = ttk.Entry(root, width=10)
    entry.insert(0, "0.5")  # Default value is 50%
    entry.grid(row=channel, column=1)
    duty_entries.append(entry)

# Label and Entry widget for PWM frequency
ttk.Label(root, text="PWM Frequency (Hz):").grid(row=17, column=0)
freq_entry = ttk.Entry(root, width=10)
freq_entry.insert(0, "1500")  # Default frequency is 1500 Hz
freq_entry.grid(row=17, column=1)

# Load the image and create a label to display it
image_path = "VoltageOutput.png"
if os.path.exists(image_path):
    voltage_output_image = tk.PhotoImage(file=image_path)
    image_label = tk.Label(root, image=voltage_output_image)
    image_label.grid(row=0, column=2, rowspan=18)  # Adjust the row and column as needed

# Button to apply duty cycles and PWM frequency
apply_button = ttk.Button(root, text="Apply Settings", command=apply_settings)
apply_button.grid(row=18, column=0, columnspan=2)

# Button to stop the program
stop_button = ttk.Button(root, text="STOP", command=stop_program)
stop_button.grid(row=19, column=0, columnspan=2)

# Read default values from the log file at the beginning
read_default_values()

# Run the GUI main loop
root.mainloop()