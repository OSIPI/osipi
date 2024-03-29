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
# Convert a series of R1 values to the corresponding signal intensities.

R1 = np.array([0.0, 1.5, 3.0, 4.0, 10.0])  # R1 in units of /s
k = np.float64(150.0)  # constant of proportionality in units of arb. unit s
signal = osipi.R1_to_s_linear(R1, k)  # signal in arb. unit
print(f'Signal: {signal}')

# Plot signal vs. R1
plt.plot(R1, signal, 'ro-')
plt.xlabel('R1 (/sec)')
plt.ylabel('signal (arb. unit)')
plt.show()