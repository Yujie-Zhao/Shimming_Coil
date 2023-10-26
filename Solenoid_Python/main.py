#
# Solenoid calculator
# Calculation of the magnetic field strength H (A/m and Oe) directed and distributed along the axis of the solenoid.
#
# Yujie Zhao, University of St. Andrews, Scotland
# 27.04.2023
#

import numpy as np
import matplotlib.pyplot as plt
pi = np.pi  # 3.1415...

# Console application:
print("")
print("The solenoid is symmetrical about 0: z0 = [-maxz0, maxz0]")
L = float(input("Enter the solenoid length L in meters: "))
R = float(input("Enter the solenoid internal radius R in meters: "))
d0 = float(input("Enter the wire diameter d0 without isolation in meters: "))
delta = float(input("Enter the wire isolation thickness in meters: "))
M = int(input("Enter the number M of winding layers: "))
maxz0 = float(input("Enter the range maxz0 for z0 = [-maxz0, maxz0] in meters: "))
I = float(input("Enter the current I in amperes: "))

# Solenoid and wire geometrical parameters:
#I = 1  # current in amperes
#R = 1.0e-2  # solenoid internal radius in meters
#L = 2.0e-1  # solenoid length in meters
#M = 6  # number of winding layers
#d0 = 1.0e-3  # wire diameter without isolation in meters
#delta = 0.0  # wire isolation thickness in meters
#maxz0 = L/2.0  # z0 = [-maxz0,+maxz0] is the range of the z-coordinate along the solenoid axis

# Derived parameters:
d = d0 + 2 * delta  # total wire diameter, including isolation
N = int(L / d) + 1  # number of turns in each layer
K = N  # number of points of the z-coordinate used for drawing the magnetic field strength
gamma = d / (2.0 * pi)  # m/rad is the rotation-to-displacement coefficient
psi = pi * N  # 2 * psi is the total rotation angle for all turns in rad

# Magnetic field strength H measured in A/m along the solenoid axis as a function of z0
def Hz(z0):
    value = 0.0
    for m in range(1, M + 1):
        value = value + (z0 + gamma * psi) / ((R + d * (2 * m - 1) / 2)**2 + (z0 + gamma * psi)**2)**0.5
        value = value - (z0 - gamma * psi) / ((R + d * (2 * m - 1) / 2)**2 + (z0 - gamma * psi)**2)**0.5
    return value * I / (4.0 * pi * gamma)

dz = 2 * maxz0 / K  # coordinate step
z = []  # list of the coordinate points along the solenoid axis in m
H1 = []  # list of the magnetic field points in A/m
for i in range(K + 1):
    z0 = -maxz0 + dz * i
    z.append(z0)
    H1.append(Hz(z0))

z = np.array(z)  # converting into an array
H1 = np.array(H1)  # converting into an array
H2 = (H1 * 4.0 * pi) / 1000  # array of the magnetic field points in Oe

stacked_array = np.column_stack((z, H1, H2))
header = "z0 (m), H (A/m), H (Oe)\n"
with open("Solenoid_Field.txt", "w") as f:
    f.write(header)
    np.savetxt(f, stacked_array, delimiter=",")

# Create two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Plot the first graph (z, H1)
ax1.plot(z, H1)
ax1.set_xlabel("z0 (m)")
ax1.set_ylabel("Hz (A/m)")
ax1.grid(True)

# Plot the second graph (z, H2)
ax2.plot(z, H2)
ax2.set_xlabel("z0 (m)")
ax2.set_ylabel("Hz (Oe)")
ax2.grid(True)

# Display the plots
plt.show()