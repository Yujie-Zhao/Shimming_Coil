#
# This Python code is used to test the PWM driver and draw its voltage characteristics.
# Use this Python program to control four PWM outputs on Arduino and measure its four analog inputs.
# Plotting graphs Vout(PWM) vs. duty cycle.
# Four PWM outputs on Arduino: duty cycle sweep from 0 to 100%.
#

import serial
import time
import numpy as np
import matplotlib.pyplot as plt

# This time delay (s) must be much larger (x5 or more) than the RC characteristic time of the RC filter
time_delay = 0.2

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)

# Wait for the Arduino to reset
time.sleep(1)

# Define constant duty cycle values
duty_cycle1 = 0  # PWM pin 1
duty_cycle2 = 0  # PWM pin 2
duty_cycle3 = 0  # PWM pin 3
duty_cycle4 = 0  # PWM pin 4

# Set initial duty cycles on Arduino
ser.write(f"{duty_cycle1} {duty_cycle2} {duty_cycle3} {duty_cycle4} \n".encode())
time.sleep(1)

# ADC properties
ADC_resolution = 1023  # ADC resolution (10-bit)
reference_voltage = 5.0  # Reference voltage (5V)

# Main loop
duty_cycle = []  # 8-bit resolution
volt1 = []
volt2 = []
volt3 = []
volt4 = []
for i in range(1, 257):
    # Read analog values from Arduino
    data = ser.readline().decode().strip().split(",")
    time.sleep(1)

    if len(data) == 4:
        try:
            analog_value1 = int(data[0])
            analog_value2 = int(data[1])
            analog_value3 = int(data[2])
            analog_value4 = int(data[3])

            # Convert analog readings to voltage
            voltage1 = (analog_value1 / ADC_resolution) * reference_voltage
            voltage2 = (analog_value2 / ADC_resolution) * reference_voltage
            voltage3 = (analog_value3 / ADC_resolution) * reference_voltage
            voltage4 = (analog_value4 / ADC_resolution) * reference_voltage
            volt1.append(voltage1)
            volt2.append(voltage2)
            volt3.append(voltage3)
            volt4.append(voltage4)

            # Print voltage values
            print(f"Voltage 1: {voltage1}V")
            print(f"Voltage 2: {voltage2}V")
            print(f"Voltage 3: {voltage3}V")
            print(f"Voltage 4: {voltage4}V")

            # Control duty cycles
            value = (i * 100.0)/256
            duty_cycle.append(value)
            new_duty_cycle1 = i  # Calculate the desired duty cycle for PWM pin 1
            new_duty_cycle2 = i  # Calculate the desired duty cycle for PWM pin 2
            new_duty_cycle3 = i  # Calculate the desired duty cycle for PWM pin 3
            new_duty_cycle4 = i  # Calculate the desired duty cycle for PWM pin 4
            print(f"Duty cycle: {value}%")
            print('')

            # Send new duty cycles to Arduino
            ser.write(f"{new_duty_cycle1} {new_duty_cycle2} {new_duty_cycle3} {new_duty_cycle4}\n".encode())
            time.sleep(time_delay)

        except ValueError:
            print("Invalid data received from Arduino")

    else:
        print("Invalid data format received from Arduino")

# Set initial duty cycles on Arduino
duty_cycle1 = 0  # PWM pin 1
duty_cycle2 = 0  # PWM pin 2
duty_cycle3 = 0  # PWM pin 3
duty_cycle4 = 0  # PWM pin 4

ser.write(f"{duty_cycle1} {duty_cycle2} {duty_cycle3} {duty_cycle4} \n".encode())
time.sleep(1)

# Close the serial connection
ser.close()

duty_cycle = np.array(duty_cycle)
volt1 = np.array(volt1)
volt2 = np.array(volt2)
volt3 = np.array(volt3)
volt4 = np.array(volt4)

# Plotting the graph
plt.plot(duty_cycle, volt1)
plt.plot(duty_cycle, volt2)
plt.plot(duty_cycle, volt3)
plt.plot(duty_cycle, volt4)
plt.xlabel("Duty cycle, %")
plt.ylabel("Output voltage, V")
plt.title("Output voltages vs. Duty cycle")
plt.grid(True)

# Displaying the graph
plt.show()