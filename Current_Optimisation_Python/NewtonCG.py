#
# The Newton-CG optimization method is used to calculate the current profile when spiral coils are stacked together.
#
from tkinter import simpledialog
import tkinter as tk
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from ResidualB import B0

pi = 3.1415926535897932384626433832795
mu0 = 4.0 * pi * 1.0e-7  # vacuum magnetic permeability

def CurrentOptimisation(tolerance, L0, L, d0, delta, h, R, Rs, w, rho, Inoise):
    #Derived parameters and arrays:
    d = d0 + 2.0 * delta
    R = d * int(R / d) + d / 2.0  # adjusted internal radius
    Rs = d * int(Rs / d) + d / 2.0  # adjusted external radius for the current optimization
    gamma = d / (2.0 * pi)
    theta1 = (2.0 * pi * R) / d - pi
    theta2 = (2.0 * pi * Rs) / d - pi
    gtd1 = 2.0 * gamma * theta1 + d
    gtd2 = 2.0 * gamma * theta2 + d
    turns = int(Rs / d) - int(R / d)  # number of full turns in each spiral for the current optimization

    # Spiral length and resistance
    val1 = (4.0 * gamma**2 + gtd1**2)**0.5
    val2 = (4.0 * gamma**2 + gtd2**2)**0.5
    sp_length = (gtd2/(8.0 * gamma)) * val2 - (gtd1/(8.0 * gamma)) * val1 + \
            (gamma / 2) * np.log((gtd2 + val2) / (gtd1 + val1))
    wire_resistance = rho * sp_length / ((pi / 4.0) * d0**2)
    strip_resistance = rho * sp_length / (d0 * h)

    M = int(L/w)  # number of the spiral coils; must be odd
    M = M + 1 if M % 2 == 0 else M + 2
    zm = np.array(list(map(lambda m: -((M - 1)/2) * w + w * m, range(M))))  # coordinates of the spirals for [-L/2,L/2]
#   print('number of the spiral coils = ', M)

    Q = int(L0/w)  # number of the induction sampling points; must be odd
    Q = Q + 1 if Q % 2 == 0 else Q + 2
    zq = np.array(list(map(lambda q: -((Q - 1)/2) * w + w * q, range(Q))))  # induction sampling points for [-L0/2,L0/2]
    b0 = np.array(list(map(lambda q: B0(zq[q]), range(Q))))  # sampling of the residual induction in Tesla
    averb0 = sum(b0[q] for q in range(Q)) / Q

    plt.plot(zq, b0)
    plt.xlabel("z0, m")
    plt.ylabel("B0, T")
    plt.title("Residual induction")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2D array of coefficients in Eq. (21) in the report
    Imcoeff = []
    for m in range(M):
        row = []
        for q in range(Q):
            sqrt_term = lambda gtd: (gtd ** 2 + 4.0 * (zq[q] - zm[m]) ** 2) ** 0.5
            value1 = gtd1 + sqrt_term(gtd1)
            value2 = gtd2 + sqrt_term(gtd2)
            value = np.log(value2 / value1) + gtd1 / sqrt_term(gtd1) - gtd2 / sqrt_term(gtd2)
            row.append(value)
        Imcoeff.append(row)
    Imcoeff = np.array(Imcoeff)

    # Initial values for the current in Eq. (23) in the report
    q0 = int((Q - 1) / 2)  # middle point where z0 = 0
    field = sum(Imcoeff[m][q0] for m in range(M))
    initial_value = -4.0 * pi * gamma * averb0 / (mu0 * field)
    x0 = [initial_value] * M

    def get_initial_current_value(window, initial_value):
        #root = tk.Tk()
        root.withdraw()
        response = simpledialog.askstring("Input",
                                          f"Suggested initial current for the optimization = {initial_value} A\n"
                                          "If the optimization does not work, propose a new value,"
                                          " choosing it as small as possible.\n"
                                          "You may try zero and then other values in small increments.\n"
                                          "Would you like to change? (y/n)",
                                          parent=window)
        if response.lower() == 'y':
            new_value = simpledialog.askfloat("Input", "Enter your initial current value in A:",
                                              parent=window)
            if new_value is not None:
                return new_value
        return initial_value

    root = tk.Tk()
    def run_main():
        value = get_initial_current_value(root, initial_value)
        I0 = [value] * M
        return I0
    x0 = run_main()

    def on_run_button_click():
        x0 = run_main()

    # 2D array of coefficients in Eq. (21) in the report
    dBz = []
    for m in range(M):
        row = []
        for q in range(Q):
            value = (mu0 / (4.0 * pi * gamma)) * Imcoeff[m][q]
            row.append(value)
        dBz.append(row)
    dBz = np.array(dBz)

    # Hessian matrix in Eq. (22) in the report
    HM = []
    for m in range(M):
        row = []
        for n in range(M):
            value = 2.0 * sum(dBz[m][q] * dBz[n][q] for q in range(Q))
            row.append(value)
        HM.append(row)
    HM = np.array(HM)

    # Hessian as a function but the variable is not used since it is a constant matrix
    def HJ(x):
        return HM

    # Function in Eq. (21) in the report
    # x is the current array used in the external iterations in Eq. (18)
    def Bz(x, q):
        return (mu0 / (4.0 * pi * gamma)) * sum(x[m] * Imcoeff[m][q] for m in range(M))

    # Gradient function in Eq. (21) in the report
    def GJ(x):
        output = []
        for m in range(M):
            value = sum(2.0 * (Bz(x, q) + b0[q]) * dBz[m][q] for q in range(Q))
            output.append(value)
        return np.array(output)

    # Least square function (15) used for the optimisation
    def fun(x):
        return sum((Bz(x, q) + b0[q])**2 for q in range(Q))

    # Minimisation algorithm:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#id1
    result = minimize(fun, x0, method = 'Newton-CG', jac = GJ, hess = HJ, tol = tolerance)
    current = np.array(result.x)
    noise_current = (lambda x: x + np.random.uniform(-Inoise, Inoise, size=x.shape))(current)
    wire_current_power = sum(map(lambda I: wire_resistance * I**2, current))
    strip_current_power = sum(map(lambda I: strip_resistance * I ** 2, current))

    with open('design_parameters_for_currents.txt', 'w') as file:
        file.write(f'strip thickness = {h} m\n')
        file.write(f'conductor diameter/width without isolation/gap = {d0} m\n')
        file.write(f'total conductor diameter/width = {d} m\n')
        file.write(f'total substrate width, including the wire diameter = {w} m\n')
        file.write(f'residual induction length = {L0} m\n')
        file.write(f'total optimisation length = {L} m\n')
        file.write(f'adjusted internal radius = {R} m\n')
        file.write(f'adjusted external radius = {Rs} m\n')
        file.write(f'number of spiral turns = {turns}\n')
        file.write(f'each spiral length = {sp_length} m\n')
        file.write(f'wire spiral resistance = {wire_resistance} Ohms\n')
        file.write(f'strip spiral resistance = {strip_resistance} Ohms\n')
        file.write(f'power dissipated in the whole wire stack = {wire_current_power} W\n')
        file.write(f'power dissipated in the whole strip stack = {strip_current_power} W\n')

    error = [lambda q: (Bz(current, q) + b0[q]) for q in range(Q)]
    noise_error = [lambda q: (Bz(noise_current, q) + b0[q]) for q in range(Q)]
    error = np.array([func(q) for q, func in enumerate(error)])
    noise_error = np.array([func(q) for q, func in enumerate(noise_error)])

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

    # Plot 1: Current profile
    plot_and_save_data(zm, current, "Current profile", "z0, m", "I, A", "current_profile.csv")

    # Plot 2: Error profile
    plot_and_save_data(zq, error, "Error profile", "z0, m", "Error, T", "error_profile.csv")

    # Plot 3: Induction profile before and after optimization
    plot_and_save_data_with_legend(zq, b0, zq, error, "Induction profile before and after optimization", "z0, m",
                                       "Induction, T", "induction_profile.csv")

    # Plot 4: Induction profile with current uncertainty
    plot_and_save_data_with_legend(zq, b0, zq, noise_error,
                                    "Induction profile before and after optimization:\n with the current uncertainty",
                                    "z0, m", "Induction, T", "induction_profile_with_uncertainty.csv")
