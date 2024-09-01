"""
=============
The Two Compartment Exchange Model
=============

Simulating tissue concentrations from two compartment models with different settings.
"""

import matplotlib.pyplot as plt

# %%
# Import necessary packages
import numpy as np
import osipi

# %%
# Generate Parker AIF with default settings.

# Define time points in units of seconds - in this case we use a time
# resolution of 1 sec and a total duration of 6 minutes.
t = np.arange(0, 6 * 60, 1)

# Create an AIF with default settings
ca = osipi.aif_parker(t)

# %%
# Plot the tissue concentrations for an extracellular volume fraction
# of 0.2, plasma volume fraction of 0.3, extraction fraction of 0.15
# and flow rate of 0.2 ml/min
E = 0.15  # Extraction fraction
Fp = 0.2  # Flow rate in ml/min
Ve = 0.2  # Extracellular volume fraction
Vp = 0.3  # Plasma volume fraction
ct = osipi.two_cxm(t, ca, E=E, Fp=Fp, Ve=Ve, Vp=Vp)
plt.plot(t, ct, "b-", label=f"E = {E}, Fp = {Fp}, Ve = {Ve}, Vp = {Vp}")
plt.xlabel("Time (sec)")
plt.ylabel("Tissue concentration (mM)")
plt.show()
