"""
==============
Linear model for relationship between R_1 and magnitude signal S
==============

Demonstrating the linear model for relationship between R_1 and magnitude signal, S = k.R_1
"""

# %%
# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import osipi

# %%
# Convert a series of R1 values to the corresponding signal intensities.

R_1 = np.array([0.0, 1.5, 3.0, 4.0, 10.0])  # R_1 in units of /s
k = np.float64(150.0)  # constant of proportionality in units of a.u. s
S = osipi.R1_to_S_linear(R_1, k)  # signal in a.u.
print(f'Signal: {S}')

# Plot S vs. R_1
plt.plot(R_1, S, 'ro-')
plt.xlabel('R_1 (/sec)')
plt.ylabel('S (a.u.)')
plt.show()