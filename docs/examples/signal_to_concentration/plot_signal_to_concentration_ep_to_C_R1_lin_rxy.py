"""
==============
Electromagnetic property inverse model: longitudinal relaxation rate, linear with relaxivity
==============

Demonstrating the inverse linear relaxivity model for converting R_1 to tissue indicator concentration C.
"""

# %%
# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import osipi

# %%
# Convert a series of R_1 values to the corresponding indicator concentrations.
R_1 = np.array([1, 2, 3, 4, 5, 6], dtype=np.float64)
R_10 = np.float64(1)
r_1 = np.float64(5)

C = osipi.ep_to_C_R1_lin_rxy(R_1, R_10, r_1)
print(f'Concentration (mM): {C}')

# Plot C vs. R_1
plt.plot(R_1, C, 'r-')
plt.xlabel('R_1 (/s)')
plt.ylabel('C (a.u.)')
plt.show()
