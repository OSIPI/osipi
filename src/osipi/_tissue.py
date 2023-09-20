import numpy as np
from scipy.interpolate import interp1d
from osipi import exp_conv


def tofts(t: np.ndarray, ca: np.ndarray, Ktrans: float, ve: float, t_offset: float = 0.0,
          discretization_method: str = "conv") -> np.ndarray:
    """Tofts model as defined by zzz et al (year)

    Args:
        t (np.ndarray): array of time points in units of sec. [OSIPI code Q.GE1.004]
        ca (np.ndarray): Arterial concentrations in mM for each time point in t. [OSIPI code Q.IC1.001]
        Ktrans (float): Volume transfer constant in units of 1/min. [OSIPI code Q.PH1.008]
        ve (float): Relative volume fraction of the extracellular extravascular compartment (e). [OSIPI code Q.PH1.001.[e]]
        t_offset (float, optional): Difference in onset time between tissue curve and aif in units of sec. [OSIPI code ????]
        discretization_method (str, optional): Defines the discretization method used in the model definition. [OSIPI code ????]

    Returns:
        np.ndarray: Tissue concentrations in mM for each time point in t.

    See Also:
        'extended_tofts'

    References:
        - Lexicon url:
        - Lexicon code: M.IC1.004
        - OSIPI name: Tofts Model
        - Adapted from contributions by: LEK_UoEdinburgh_UK, ST_USyd_AUS

    Example:

        Create an array of time points covering 6min in steps of 1sec, calculate the Parker AIF at these time points and plot the results.

        Import packages:

        >>> import matplotlib.pyplot as plt
        >>> import osipi

        Calculate AIF

        >>> t = np.arange(0, 6*60, 0.1)
        >>> ca = osipi.aif_parker(t)

        Calculate tissue concentrations and plot
        >>> Ktrans = 0.6 # in units of 1/min
        >>> ve = 0.2 # takes values from 0 to 1
        >>> ct = osipi.tofts(t, ca, Ktrans, ve)
        >>> plt.plot(t, ca, 'r', t, ct, 'b')
    """

    # Convert from OSIPI units (sec) to mins
    t_min = t / 60
    t_off_min = t_offset / 60

    # Shift the AIF by the toff (if not zero)
    if t_off_min != 0:
        f = interp1d(t, ca, kind='linear', bounds_error=False, fill_value=0)
        ca = (t_min > t_off_min) * f(t_min - t_off_min)

    if discretization_method == 'exp_conv':  # Use exponential convolution
        Tc = ve / Ktrans
        ct = ve * exp_conv(Tc, t_min, ca)

    else:  # Use convolution by default
        # Calculate the impulse response function
        imp = Ktrans * np.exp(-1 * Ktrans * t / ve)

        # Convolve impulse response with AIF
        convolution = np.convolve(ca, imp)

        # Discard unwanted points and make sure time spacing is correct
        ct = convolution[0:len(t_min)] * t_min[1]

    return ct
