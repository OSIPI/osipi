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
t = np.arange(0, 5 * 60, 1, dtype=float)

# Create an AIF with default settings
ca = osipi.aif_parker(t)

# %%
# Plot the tissue concentrations for an extracellular volume fraction
# of 0.2, plasma volume fraction of 0.1, permeability serface area of 5 ml/min
# and flow rate of 10 ml/min
PS = 15  # Permeability surface area product in ml/min
Fp = [10, 25]  # Flow rate in ml/min
ve = 0.1  # Extracellular volume fraction
vp = [0.1, 0.02]  # Plasma volume fraction

ct = osipi.two_compartment_exchange_model(t, ca, Fp=Fp[0], PS=PS, ve=ve, vp=vp[0])
plt.plot(t, ct, "b-", label=f" Fp = {Fp[0]},PS = {PS}, ve = {ve}, vp = {vp[0]}")

ct = osipi.two_compartment_exchange_model(t, ca, Fp=Fp[1], PS=PS, ve=ve, vp=vp[0])
plt.plot(t, ct, "r-", label=f" Fp = {Fp[1]},PS = {PS}, ve = {ve}, vp = {vp[0]}")

ct = osipi.two_compartment_exchange_model(t, ca, Fp=Fp[0], PS=PS, ve=ve, vp=vp[1])
plt.plot(t, ct, "g-", label=f" Fp = {Fp[0]},PS = {PS}, ve = {ve}, vp = {vp[1]}")

ct = osipi.two_compartment_exchange_model(t, ca, Fp=Fp[1], PS=PS, ve=ve, vp=vp[1])
plt.plot(t, ct, "y-", label=f" Fp = {Fp[1]},PS = {PS}, ve = {ve}, vp = {vp[1]}")


plt.xlabel("Time (sec)")
plt.ylabel("Tissue concentration (mM)")
plt.legend()
plt.show()
