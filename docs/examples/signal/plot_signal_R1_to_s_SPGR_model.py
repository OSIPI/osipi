"""
==============
Linear model for relationship between R1 and magnitude signal
==============

Demonstrating the linear model for relationship between R1 and magnitude signal, s = k.R1
"""

# %%
# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import osipi

# %%
# Convert a series of R_1 values to the corresponding signal intensities using the SPGR model.

R_1 = np.linspace(0.1, 10, 50)  # R_1 in units of /s.
S_0 = np.float64(100)  # fully T1-relaxed signal in units of a.u.
TR = np.float64(5e-3)  # repetition time in units of s.
a = np.float64(15)  # prescribed flip angle in units of deg.
S = osipi.R1_to_S_SPGR_model(R_1, S_0, TR, a)  # signal in a.u.
print(f'Signal: {S}')

# Plot S vs. R_1
plt.plot(R_1, S, 'r-')
plt.xlabel('R_1 (/sec)')
plt.ylabel('S (a.u.)')
plt.show()
