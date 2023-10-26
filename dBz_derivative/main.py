#
# This code is used to symbolically calculate the derivatives in Eqs. (33), (34)
#

import sympy as sp
import textwrap

# Define the variables in your expression
x, d, gamma, theta1, theta2, gtd1, gtd2, a, zm, zq, pi, mu0, I = sp.symbols('x, d, gamma, theta1, theta2, gtd1, gtd2,'
                                                                            ' a, zm, zq, pi, mu0, I')

def bz(x):
    theta2 = theta1 + x * sp.tanh(a * x)
    gtd2 = 2.0 * gamma * theta2 + d
    value1 = gtd1 + (gtd1 ** 2 + 4.0 * (zq - zm) ** 2) ** 0.5
    value2 = gtd2 + (gtd2 ** 2 + 4.0 * (zq - zm) ** 2) ** 0.5
    value = (sp.log(value2 / value1) + gtd1 / ((gtd1 ** 2 + 4.0 * (zq - zm) ** 2) ** 0.5)
             - gtd2 / ((gtd2 ** 2 + 4.0 * (zq - zm) ** 2) ** 0.5))
    bz_value = sp.tanh(a * x) * value
    return mu0 * I * bz_value / (4.0 * pi * gamma)

expression = bz(x)

# Calculate the partial derivative with respect to x
partial_derivative = sp.diff(expression, x)

# Simplify the result
simplified_derivative = sp.simplify(partial_derivative)

# Convert the simplified result to a string
result_str = str(simplified_derivative)

# Define the maximum line width
max_line_width = 80  # Adjust this value to fit your window width

# Wrap the lines to fit within the specified width
wrapped_lines = textwrap.wrap(result_str, width=max_line_width)

# Print the wrapped lines
for line in wrapped_lines:
    print(line)
