import numpy as np
from scipy.interpolate import interp1d
from ._convolution import exp_conv


def tofts(t: np.ndarray, ca: np.ndarray, Ktrans: float, ve: float, Ta: float = 30.0,
          discretization_method: str = "conv") -> np.ndarray:

    """Tofts model as defined by Tofts and Kermode (1991)

    Args:
        t (np.ndarray): array of time points in units of sec. [OSIPI code Q.GE1.004]
        ca (np.ndarray): Arterial concentrations in mM for each time point in t. [OSIPI code Q.IC1.001]
        Ktrans (float): Volume transfer constant in units of 1/sec. [OSIPI code Q.PH1.008]
        ve (float): Relative volume fraction of the extracellular extravascular compartment (e). [OSIPI code Q.PH1.001.[e]]
        Ta (float, optional): Arterial delay time, i.e., difference in onset time between tissue curve and AIF in units of sec. Defaults to 30 seconds. [OSIPI code Q.PH1.007]
        discretization_method (str, optional): Defines the discretization method. Options include

            – 'conv': Numerical convolution (default) [OSIPI code G.DI1.001]

            – 'exp': Exponential convolution [OSIPI code G.DI1.006]


    Returns:
        np.ndarray: Tissue concentrations in mM for each time point in t.

    See Also:
        `extended_tofts`

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#indicator-kinetic-models
        - Lexicon code: M.IC1.004
        - OSIPI name: Tofts Model
        - Adapted from contributions by: LEK_UoEdinburgh_UK, ST_USyd_AUS, MJT_UoEdinburgh_UK

    Example:

        Create an array of time points covering 6 min in steps of 1 sec, calculate the Parker AIF at these time points, calculate tissue concentrations
        using the Tofts model and plot the results.

        Import packages:

        >>> import matplotlib.pyplot as plt
        >>> import osipi
        >>> import numpy

        Calculate AIF:

        >>> t = np.arange(0, 6*60, 1)
        >>> ca = osipi.aif_parker(t)

        Calculate tissue concentrations and plot:
        >>> Ktrans = 0.6/60 # in units of 1/sec
        >>> ve = 0.2 # takes values from 0 to 1
        >>> ct = osipi.tofts(t, ca, Ktrans, ve)
        >>> plt.plot(t, ca, 'r', t, ct, 'b')
    """

    # Shift the AIF by the arterial delay time (if not zero)
    if Ta != 0:
        f = interp1d(t, ca, kind='linear', bounds_error=False, fill_value=0)
        ca = (t > Ta) * f(t - Ta)

    if discretization_method == 'exp':  # Use exponential convolution
        try:
            Tc = ve / Ktrans
        except ZeroDivisionError:
            print('Division by zero error: Ktrans assigned 0')
            ct = 0 * ca
        else:
            ct = ve * exp_conv(Tc, t, ca)

    else:  # Use convolution by default
        # Calculate the impulse response function
        try:
            kep = Ktrans / ve
        except ZeroDivisionError:
            print('Division by zero: ve assigned 0')
            ct = ca
        else:
            imp = Ktrans * np.exp(-1 * kep * t)

            # Check if time data grid is uniformly spaced
            if np.allclose(np.diff(t), np.diff(t)[0]):
                # Convolve impulse response with AIF
                convolution = np.convolve(ca, imp)

                # Discard unwanted points and make sure time spacing is correct
                ct = convolution[0:len(t)] * t[1]
            else:
                # Print WARNING - non-uniform time grid detected - resampling
                # Resample at the smallest spacing
                dt = np.min(np.diff(t))
                t_resampled = np.linspace(t[0], t[-1], int((t[-1]-t[0])/dt))
                ca_func = interp1d(t, ca, kind='quadratic', bounds_error=False, fill_value=0)
                imp_func = interp1d(t, imp, kind='quadratic', bounds_error=False, fill_value=0)
                ca_resampled = ca_func(t_resampled)
                imp_resampled = imp_func(t_resampled)
                # Convolve impulse response with AIF
                convolution = np.convolve(ca_resampled, imp_resampled)

                # Discard unwanted points and make sure time spacing is correct
                ct_resampled = convolution[0:len(t_resampled)] * t_resampled[1]

                # Restore time grid spacing
                ct_func = interp1d(t_resampled, ct_resampled, kind='quadratic', bounds_error=False, fill_value=0)
                ct = ct_func(t)

    return ct


def extended_tofts(t: np.ndarray, ca: np.ndarray, Ktrans: float, ve: float, Ta: float = 30.0,
          discretization_method: str = "conv") -> np.ndarray:
    """Extended tofts model as defined by ???.

    Note:
        This function is not yet implemented. If you are implementing it yourself please consider submitting a code contribution to OSIPI, so nobody ever has to write this function again!

    Args:
        t (np.ndarray): array of time points in units of sec. [OSIPI code Q.GE1.004]
        ca (np.ndarray): Arterial concentrations in mM for each time point in t. [OSIPI code Q.IC1.001]
        Ktrans (float): Volume transfer constant in units of 1/sec. [OSIPI code Q.PH1.008]
        ve (float): Relative volume fraction of the extracellular extravascular compartment (e). [OSIPI code Q.PH1.001.[e]]
        Ta (float, optional): Arterial delay time, i.e., difference in onset time between tissue curve and AIF in units of sec. Defaults to 30 seconds. [OSIPI code Q.PH1.007]
        discretization_method (str, optional): Defines the discretization method. Options include

            – 'conv': Numerical convolution (default) [OSIPI code G.DI1.001]

            – 'exp': Exponential convolution [OSIPI code G.DI1.006]


    Returns:
        np.ndarray: Tissue concentrations in mM for each time point in t.

    See Also:
        `tofts`

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#indicator-kinetic-models
        - Lexicon code: M.IC1.005
        - OSIPI name: Extended Tofts Model
        - Adapted from contributions by: TBC

    Example:

        Create an array of time points covering 6min in steps of 1sec, calculate the Parker AIF at these time points, calculate tissue concentrations
        using the Extended Tofts model and plot the results.

        Import packages:

        >>> import matplotlib.pyplot as plt
        >>> import osipi

        Calculate AIF

        >>> t = np.arange(0, 6*60, 0.1)
        >>> ca = osipi.aif_parker(t)

        Calculate tissue concentrations and plot
        >>> Ktrans = 0.6/60 # in units of 1/sec
        >>> ve = 0.2 # takes values from 0 to 1
        >>> ct = osipi.extended_tofts(t, ca, Ktrans, ve)
        >>> plt.plot(t, ca, 'r', t, ct, 'b')
    """

    msg = 'This function is not yet implemented \n'
    msg += 'If you implement it yourself, please consider submitting it as an OSIPI code contribution'
    raise NotImplementedError(msg)

