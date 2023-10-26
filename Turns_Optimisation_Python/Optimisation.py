#
# The Optimisation methods are used to calculate the turns profile when spiral coils are stacked together.
#

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from ResidualB import B0

pi = 3.1415926535897932384626433832795
mu0 = 4.0 * pi * 1.0e-7  # vacuum magnetic permeability

def TurnsOptimisation(tolerance, L0, L, d0, delta, h, R, a, w, rho, I, N, Method):
    M = int(L/w)  # number of the spiral coils; must be odd
    M = M + 1 if M % 2 == 0 else M + 2
    zm = np.array(list(map(lambda m: -((M - 1)/2) * w + w * m, range(M))))  # coordinates of the spirals for [-L/2,L/2]

    Q = int(L0/w)  # number of the induction sampling points; must be odd
    Q = Q + 1 if Q % 2 == 0 else Q + 2
    zq = np.array(list(map(lambda q: -((Q - 1)/2) * w + w * q, range(Q))))  # induction sampling points for [-L0/2,L0/2]
    b0 = np.array(list(map(lambda q: B0(zq[q]), range(Q))))  # sampling of the residual induction in Tesla

    plt.plot(zq, b0)
    plt.xlabel("z0, m")
    plt.ylabel("B0, T")
    plt.title("Residual induction")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Some initial constants used in the functions
    d = d0 + 2.0 * delta  # total conductor diameter including the isolation
    R = d * int(R / d) + d / 2.0  # adjusted internal radius
    gamma = d / (2.0 * pi)
    theta1 = (2.0 * pi * R) / d - pi
    gtd1 = 2.0 * gamma * theta1 + d

    # Function in Eq. (32) in the report
    def Bz(x, q):
        Bz_value = 0.0
        for m in range(M):
            theta2 = theta1 + x[m] * np.tanh(a * x[m])
            gtd2 = 2.0 * gamma * theta2 + d
            sqrt_term = lambda gtd: (gtd ** 2 + 4.0 * (zq[q] - zm[m]) ** 2) ** 0.5
            value1 = gtd1 + sqrt_term(gtd1)
            value2 = gtd2 + sqrt_term(gtd2)
            value = np.log(value2 / value1) + gtd1 / sqrt_term(gtd1) - gtd2 / sqrt_term(gtd2)
            Bz_value = Bz_value + np.tanh(a * x[m]) * value
        return mu0 * I * Bz_value / (4.0 * pi * gamma)

    # Induction function used for testing the optimisation (step signature function)
    def Bz_test(x, q):
        Bz_value = 0.0
        for m in range(M):
            if x[m] < 0.0:
                theta2 = theta1 - x[m]
            else:
                theta2 = theta1 + x[m]
            gtd2 = 2.0 * gamma * theta2 + d
            sqrt_term = lambda gtd: (gtd ** 2 + 4.0 * (zq[q] - zm[m]) ** 2) ** 0.5
            value1 = gtd1 + sqrt_term(gtd1)
            value2 = gtd2 + sqrt_term(gtd2)
            value = np.log(value2 / value1) + gtd1 / sqrt_term(gtd1) - gtd2 / sqrt_term(gtd2)
            if x[m] < 0:
                Bz_value = Bz_value - value
            else:
                Bz_value = Bz_value + value
        return mu0 * I * Bz_value / (4.0 * pi * gamma)

    # Least square function in Eq. (31) used for the optimisation
    def fun(x):
        return sum((Bz(x, q) + b0[q])**2 for q in range(Q))

    # Derivative in Eqs. (33), (34) calculated using SymPy library (https://www.sympy.org/en/index.html)
    # During the calculations it may overflow, but will continue. Choose a proper "a" parameter.
    def dBz(x, m, q):
        b = 0.25 * I * mu0 * (a * ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**2.5 * (d
        + 2.0 * gamma * (theta1 + x * np.tanh(a * x)) + 2.0 * ((0.5 * d + gamma * (theta1 +
        x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5) * (0.5 * gtd1 * ((0.5 * d + gamma * (theta1 +
        x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5 - (0.5 * d + gamma * (theta1 +
        x * np.tanh(a * x))) * (0.25 * gtd1**2 + (zm[m] - zq[q])**2)**0.5 + (0.25 * gtd1**2 + (zm[m] -
        zq[q])**2)**0.5 * ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] -
        zq[q])**2)**0.5 * np.log((d + 2.0 * gamma * (theta1 + x * np.tanh(a * x)) + 2.0 * ((0.5 * d +
        gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5) / (gtd1 + 2.0 * (0.25 * gtd1**2
        + (zm[m] - zq[q])**2)**0.5))) / np.cosh(a * x)**2 + gamma * (0.25 * gtd1**2 + (zm[m] -
        zq[q])**2)**0.5 * (a * x / np.cosh(a * x)**2 + np.tanh(a * x)) * ((0.5 * d + gamma*(theta1 +
        x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5 * (0.5 * (0.5 * d + gamma * (theta1 +
        x * np.tanh(a * x))) * (d + 2.0 * gamma * (theta1 + x * np.tanh(a * x)))*((0.5 * d + gamma * (theta1 +
        x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2) * (d + 2.0 * gamma * (theta1 + x * np.tanh(a * x)) +
        2.0 * ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5) +
        2.0 * ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**2.0 * (0.5 * d +
        gamma * (theta1 + x * np.tanh(a * x)) + ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m]
        - zq[q])**2)**0.5) - ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] -
        zq[q])**2)**2.0 * (d + 2.0 * gamma * (theta1 + x * np.tanh(a * x)) + 2.0 * ((0.5 * d + gamma * (theta1
        + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5)) * np.tanh(a * x)) / (gamma * pi * (0.25 * gtd1**2 +
        (zm[m] - zq[q])**2)**0.5 * ((0.5 * d + gamma * (theta1 + x * np.tanh(a * x)))**2 + (zm[m] -
        zq[q])**2)**3.0 * (d + 2.0 * gamma * (theta1 + x * np.tanh(a * x)) + 2.0 * ((0.5 * d + gamma * (theta1
        + x * np.tanh(a * x)))**2 + (zm[m] - zq[q])**2)**0.5))
        return b

    # Calculation of the Jacobian in Eq. (33)
    def jac(x):
        J = np.zeros(M)
        for m in range(M):
            J[m] = 2.0 * sum((Bz(x, q) + b0[q]) * dBz(x[m], m, q) for q in range(Q))
        return np.array(J)

    # Calculation of the Hessian matrix in Eq. (34)
    def hess(x):
        HM = []
        for m in range(M):
            row = []
            for n in range(M):
                value = 2.0 * sum(dBz(x[m], m, q) * dBz(x[n], n, q) for q in range(Q))
                row.append(value)
            HM.append(row)
        HM = np.array(HM)
        return HM

    # Minimisation algorithm:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#id1
    # We will use only these four methods: trust-exact (1), trust-krylov (2), trust-ncg (3), Newton-CG (4)
    x0 = np.full(M, N * 2.0 * pi)  # array with the initial degrees (rads), where N is the initial number of turns
    if Method == 1:
        optimisation = 'trust-exact'
    elif Method == 2:
        optimisation = 'trust-krylov'
    elif Method == 3:
        optimisation = 'trust-ncg'
    else:
        optimisation = 'Newton-CG'

    result = minimize(fun, x0, method = optimisation, jac = jac, hess = hess, tol = tolerance)
    xs = np.array(result.x)  # array of the optimised values of the variable "hi" in Eq. (29)
    turns = (xs / (2.0 * pi)).astype(int)  # angles converted to the full turns
    xs_adj = turns * 2.0 * pi  # adjusted 'hi' for the full turns

    # Quality of the optimisation
    error = [lambda q: (Bz_test(xs_adj, q) + b0[q]) for q in range(Q)]
    error = np.array([func(q) for q, func in enumerate(error)])

    def plot_and_save_data(x, y, title, xlabel, ylabel, filename):
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        data = np.column_stack((x, y))
        np.savetxt(filename, data, delimiter=",")

    def plot_and_save_data_with_legend(x1, y1, x2, y2, title, xlabel, ylabel, filename):
        plt.plot(x1, y1, color='blue', label='B0')
        plt.plot(x2, y2, color='green', label='B0 + Bz')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()

        data = np.column_stack((x1, y1, y2))
        np.savetxt(filename, data, delimiter=",")

    # Plot 1: Turns profile
    plot_and_save_data(zm, turns, "Turns profile", "z0, m", "Full turns", "turns_profile.csv")

    # Plot 2: Error profile
    plot_and_save_data(zq, error, "Error profile", "z0, m", "Error, T", "error_profile.csv")

    # Plot 3: Induction profile before and after optimization
    plot_and_save_data_with_legend(zq, b0, zq, error, "Induction profile before and after optimization", "z0, m",
                                   "Induction, T", "induction_profile.csv")

    # Calculation of the individual resistances of the spiral coils and the total resistance of the stack
    wire_resistance = []
    strip_resistance = []
    spiral_length = []
    for m in range(M):
        if xs_adj[m] < 0.0:
            theta2 = theta1 - xs_adj[m]
        else:
            theta2 = theta1 + xs_adj[m]
        gtd2 = 2.0 * gamma * theta2 + d
        # Spiral length and resistance
        val1 = (4.0 * gamma**2 + gtd1**2)**0.5
        val2 = (4.0 * gamma**2 + gtd2**2)**0.5
        length = ((gtd2/(8.0 * gamma)) * val2 - (gtd1/(8.0 * gamma)) * val1 +
                     (gamma / 2) * np.log((gtd2 + val2) / (gtd1 + val1)))
        spiral_length.append(length)
        wire_resistance.append(rho * length / ((pi / 4.0) * d0**2))
        strip_resistance.append(rho * length / (d0 * h))

    # Writing the wire and microstrip resistances to the file
    data = np.column_stack((zm, spiral_length, wire_resistance, strip_resistance))
    csv_file = "length_resistance_profiles.csv"
    np.savetxt(csv_file, data, delimiter=",", header="zm(m), Length(m), R_wires(Ohms), R_strips(Ohms)", comments='')

    # Coil stack parameters
    total_spiral_length = np.sum(spiral_length)  # length (m)
    total_wire_resistance = np.sum(wire_resistance)  # resistance (Ohms)
    total_strip_resistance = np.sum(strip_resistance)  # resistance (Ohms)
    wire_current_power = total_wire_resistance * I**2  # power dissipated in the whole wire stack
    strip_current_power = total_strip_resistance * I**2  # power dissipated in the whole strip stack

    with open('design_parameters_for_turns.txt', 'w') as file:
        file.write(f'total current through all spiral coils = {I} A\n')
        file.write(f'strip thickness = {h} m\n')
        file.write(f'conductor diameter/width without isolation/gap = {d0} m\n')
        file.write(f'total conductor diameter/width = {d} m\n')
        file.write(f'total substrate width, including the wire diameter = {w} m\n')
        file.write(f'residual induction length = {L0} m\n')
        file.write(f'total optimisation length = {L} m\n')
        file.write(f'adjusted internal radius = {R} m\n')
        file.write(f'total length of the spirals = {total_spiral_length} m\n')
        file.write(f'total wire resistance = {total_wire_resistance} Ohms\n')
        file.write(f'total strip resistance = {total_strip_resistance} Ohms\n')
        file.write(f'power dissipated in the whole wire stack = {wire_current_power} W\n')
        file.write(f'power dissipated in the whole strip stack = {strip_current_power} W\n')