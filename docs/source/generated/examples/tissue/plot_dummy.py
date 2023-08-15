"""
====================
Dummy script as demo
====================

Dummy script to show the examples structure. 
"""

import numpy as np
import matplotlib.pyplot as plt
import osipi

# %%
# Generate synthetic AIF with default settings and plot the result.

# Define time points in units of seconds - in this case we use a time resolution of 0.5 sec and a total duration of 6 minutes.
t = np.arange(0, 6*60, 0.5)

# Create an AIF with default settings
ca = osipi.aif_parker(t)

# Plot the AIF over the full range
plt.plot(t, ca)
plt.show()


# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
