#
# The main module for GUI that calls the optimisation algorithms
# Yujie Zhao, University of St. Andrews, Scotland, 30th July 2023.
#

import os
from NewtonCG import *

PARAMETERS_FILE = "parameters.txt"
NUM_PARAMETERS = 11

def stop_main():
    quit()

def run_main():
    # This function will be called when the "Run" button is clicked
    # You can access the parameter values here and call your own function using the parameters

    # Retrieve the parameter values from the input fields
    params = [float(entries[i].get()) for i in range(1, NUM_PARAMETERS+1)]

    # Save the parameter values to a file
    save_parameters(params)

    # params[0] tolerance: tolerance for termination of the iteration process.
    # params[1] L0: length (m) within which the induction was measured
    # params[2] L: length (m) of the optimisation (we suggest L > L0)
    # params[3] d0: wire diameter (m) without isolation or strip width
    # params[4] delta: thickness of the wire isolation or the half-gap between the strips (m) on PCB
    # params[5] h: strip thickness (m) on PCB
    # Both radii will be slightly adjusted: R = d * int(R/d) + d/2 and Rs = d * int(Rs/d) + d/2, where d = d0 + 2*delta
    # params[6] R: internal radius (m) of the shimming coil
    # params[7] Rs: external radius (m) of the shimming coil
    # params[8] w: substrate width (m); w = d0 + 2*delta if no substrates
    # params[9] rho: conductor resistivity (Ohm*m)
    # params[10] Inoise: current uncertainty (+/-) in A caused by the driver performance

    CurrentOptimisation(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7],
                        params[8], params[9], params[10])

def save_parameters(params):
    # Save the parameter values to a file
    with open(PARAMETERS_FILE, "w") as file:
        for param in params:
            file.write(f"{param}\n")

def load_parameters():
    # Load the parameter values from the file, if it exists
    if os.path.exists(PARAMETERS_FILE):
        with open(PARAMETERS_FILE, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                entry = entries[i+1]
                entry.delete(0, tk.END)
                entry.insert(0, line.strip())
    else:
        # If the file doesn't exist, set default values for all parameters
        default_values = ["0"] * NUM_PARAMETERS
        for i, default_value in enumerate(default_values):
            entry = entries[i+1]
            entry.delete(0, tk.END)
            entry.insert(0, default_value)
        # Save the default values to the file
        save_parameters(default_values)

# Create the main window
window = tk.Tk()
window.title("PARAMETER INPUT FOR THE CURRENT OPTIMISATION: meters, amperes, ohms. You can use the scientific format")

# Create a frame to hold the parameter labels and entry fields
frame = tk.Frame(window, bg="pink")
frame.pack(padx=20, pady=20)

# Create labels and entry fields for each parameter
param_labels = [
    'Tolerance (10^-6 or 10^-8 is recommended) for termination of the iteration process',
    'L0 - length (m) within which the induction was measured',
    'L - optimisation length (m) (choose L > L0)',
    'd0 - wire diameter (m) without isolation or strip width (m) on PCB',
    'delta - thickness (m) of the wire isolation or the half-gap between the strips on PCB',
    'h - strip thickness (m) on PCB',
    'R - internal radius (m) of the shimming coil',
    'Rs - external radius (m) of the shimming coil',
    'w - substrate width (m) including turns; w = d0 + 2*delta if no substrates (only for wires)',
    'rho - conductor resistivity (Ohm*m): 1.68e-8 Cu, 2.65e-8 Al, 1.59e-8 Ag',
    'Current +/- uncertainty (A) caused by the driver performance (estimated)'
]

entries = {}

for i, label_text in enumerate(param_labels):
    label = tk.Label(frame, text=label_text, fg="black", font=("Helvetica", 12), bg="pink", anchor=tk.W)
    label.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=5)

    entry = tk.Entry(frame, font=("Helvetica", 12), bg="pink", width=30)  # Decreased width for value field
    entry.grid(row=i, column=1, padx=(0, 20), pady=5)

    entries[i+1] = entry

# Load the saved parameters as defaults
load_parameters()

# Create a frame as a container for the buttons
button_frame = tk.Frame(window)

# Create the "Run" button
run_button = tk.Button(button_frame, text="Run", command=run_main, font=("Helvetica", 14, "bold"))
run_button.grid(row=0, column=0, padx=10)

# Create the "Stop" button
stop_button = tk.Button(button_frame, text="Stop", command=stop_main, font=("Helvetica", 14, "bold"))
stop_button.grid(row=0, column=1, padx=10)

# Center the button frame within the window
button_frame.pack(pady=10)

# Start the GUI main loop
window.mainloop()
