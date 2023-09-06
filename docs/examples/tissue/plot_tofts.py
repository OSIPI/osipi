"""
====================
The Tofts model
====================

Simulating tissue concentrations from Tofts model with different settings.
"""

# %%
# Import necessary packages
import numpy as np
import itertools
import matplotlib.pyplot as plt
import osipi

# %%
# Generate Parker AIF with default settings.

# Define time points in units of seconds - in this case we use a time resolution of 0.5 sec and a total duration of 6 minutes.
t = np.arange(0, 6*60, 0.5)

# Create an AIF with default settings
ca = osipi.aif_parker(t)

# %%
# Plot the tissue concentrations for different transfer rate constants
Ktrans = [0.05, 0.2, 0.6]  # in units of 1/min
ve = 0.2  # volume fraction  between 0 and 1
fig, axs = plt.subplots(1, 3)

for i, ax in enumerate(axs.flatten()):
    ct = osipi.tofts(t, ca, Ktrans[i], ve)
    ax.plot(t, ct)
    ax.set_title(f'Ktrans = {Ktrans[i]} /min')
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Tissue concentration (mM)')
plt.tight_layout()
plt.show()

# %%
# Comparing different discretization methods
fig, axs = plt.subplots(1, 3)

for i, ax in enumerate(axs.flatten()):
    ct_conv = osipi.tofts(t, ca, Ktrans[i], ve) # Defaults to Convolution
    ct_exp_conv = osipi.tofts(t, ca, Ktrans[i], ve, discretization_method='exp_conv')
    l1, = ax.plot(t, ct_conv, 'b-')
    l2, = ax.plot(t, ct_exp_conv, 'm-')
    ax.set_title(f'Ktrans = {Ktrans[i]} /min')
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Tissue concentration (mM)')
fig.legend((l1, l2), ('Convolution','Exponential Convolution'))
plt.tight_layout()
plt.show()

# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
