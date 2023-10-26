#
# Single-axis residual induction (T, Tesla) as a function of the z0 coordinate.
# You can use a polynomial or any other fitting function of a single variable to describe the residual field.
#

# A residual field provided by the mmWave lab at the University of St. Andrews, Scotland.
def B0(z0):
    value = -5.859e-6 + 4.766114e-3 * z0 - 0.486506371 * z0**2 - 1.4609783504e1 * z0**3 + 4.2600403748e2 * z0**4 +\
            3.04437e4 * z0**5 - 8.75637e5 * z0**6 - 7.65903e6 * z0**7 + 1.46997e8 * z0**8
    return value

