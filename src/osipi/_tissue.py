import warnings

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import convolve

from ._convolution import exp_conv


def tofts(
    t: np.ndarray,
    ca: np.ndarray,
    Ktrans: float,
    ve: float,
    Ta: float = 30.0,
    discretization_method: str = "conv",
) -> np.ndarray:
    """Tofts model as defined by Tofts and Kermode (1991)

    Args:
        t (np.ndarray): array of time points in units of sec. [OSIPI code Q.GE1.004]
        ca (np.ndarray):
            Arterial concentrations in mM for each time point in t. [OSIPI code Q.IC1.001]
        Ktrans (float):
            Volume transfer constant in units of 1/min. [OSIPI code Q.PH1.008]
        ve (float):
            Relative volume fraction of the extracellular
            extravascular compartment (e). [OSIPI code Q.PH1.001.[e]]
        Ta (float, optional):
            Arterial delay time,
            i.e., difference in onset time between tissue curve and AIF in units of sec. Defaults to 30 seconds. [OSIPI code Q.PH1.007]
        discretization_method (str, optional): Defines the discretization method. Options include

            – 'conv': Numerical convolution (default) [OSIPI code G.DI1.001]

            – 'exp': Exponential convolution [OSIPI code G.DI1.006]


    Returns:
        np.ndarray: Tissue concentrations in mM for each time point in t.

    See Also:
        `extended_tofts`

    References:
        - Lexicon url:
            https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#indicator-kinetic-models
        - Lexicon code: M.IC1.004
        - OSIPI name: Tofts Model
        - Adapted from contributions by: LEK_UoEdinburgh_UK, ST_USyd_AUS, MJT_UoEdinburgh_UK

    Example:

        Create an array of time points covering 6 min in steps of 1 sec,
        calculate the Parker AIF at these time points, calculate tissue concentrations
        using the Tofts model and plot the results.

        Import packages:

        >>> import matplotlib.pyplot as plt
        >>> import osipi
        >>> import numpy

        Calculate AIF:

        >>> t = np.arange(0, 6 * 60, 1)
        >>> ca = osipi.aif_parker(t)

        Calculate tissue concentrations and plot:

        >>> Ktrans = 0.6  # in units of 1/min
        >>> ve = 0.2  # takes values from 0 to 1
        >>> ct = osipi.tofts(t, ca, Ktrans, ve)
        >>> plt.plot(t, ca, "r", t, ct, "b")

    """

    # Input validation
    if t.size != ca.size:
        raise ValueError(f"t and ca must have the same size, got {t.size} and {ca.size}")

    for param, name in [(Ktrans, "Ktrans"), (ve, "ve"), (Ta, "Ta")]:
        if not (np.isscalar(param) and np.isreal(param)):
            raise TypeError(f"{name} must be a numeric scalar value, got {type(param).__name__}")

    if Ktrans < 0:
        raise ValueError(f"Ktrans must be non-negative, got {Ktrans}")
    if not (0 <= ve <= 1):
        raise ValueError(f"ve must be in range [0, 1], got {ve}")
    if Ta < 0:
        raise ValueError(f"Ta must be non-negative, got {Ta}")

    if not np.allclose(np.diff(t), np.diff(t)[0]):
        warnings.warn(
            ("Non-uniform time spacing detected. Time array may be" " resampled."),
            stacklevel=2,
        )

    if Ktrans <= 0 or ve <= 0:
        ct = 0 * ca

    else:
        # Convert units
        Ktrans = Ktrans / 60  # from 1/min to 1/sec

        if discretization_method == "exp":  # Use exponential convolution
            # Shift the AIF by the arterial delay time (if not zero)
            if Ta != 0:
                f = interp1d(
                    t,
                    ca,
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                ca = (t > Ta) * f(t - Ta)

            Tc = ve / Ktrans
            ct = ve * exp_conv(Tc, t, ca)

        else:  # Use convolution by default
            # Calculate the impulse response function
            kep = Ktrans / ve
            imp = Ktrans * np.exp(-1 * kep * t)

            # Shift the AIF by the arterial delay time (if not zero)
            if Ta != 0:
                f = interp1d(
                    t,
                    ca,
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                ca = (t > Ta) * f(t - Ta)

            # Check if time data grid is uniformly spaced
            if np.allclose(np.diff(t), np.diff(t)[0]):
                # Convolve impulse response with AIF
                convolution = np.convolve(ca, imp)

                # Discard unwanted points and make sure time spacing
                # is correct
                ct = convolution[0 : len(t)] * t[1]
            else:
                # Resample at the smallest spacing
                dt = np.min(np.diff(t))
                t_resampled = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / dt))
                ca_func = interp1d(
                    t,
                    ca,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                imp_func = interp1d(
                    t,
                    imp,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                ca_resampled = ca_func(t_resampled)
                imp_resampled = imp_func(t_resampled)
                # Convolve impulse response with AIF
                convolution = np.convolve(ca_resampled, imp_resampled)

                # Discard unwanted points and make sure time spacing
                # is correct
                ct_resampled = convolution[0 : len(t_resampled)] * t_resampled[1]

                # Restore time grid spacing
                ct_func = interp1d(
                    t_resampled,
                    ct_resampled,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                ct = ct_func(t)

    return ct


def extended_tofts(
    t: np.ndarray,
    ca: np.ndarray,
    Ktrans: float,
    ve: float,
    vp: float,
    Ta: float = 30.0,
    discretization_method: str = "conv",
) -> np.ndarray:
    """Extended tofts model as defined by Tofts (1997)

    Args:
        t (np.ndarray):
            array of time points in units of sec. [OSIPI code Q.GE1.004]
        ca (np.ndarray):
            Arterial concentrations in mM for each time point in t. [OSIPI code Q.IC1.001]
        Ktrans (float):
            Volume transfer constant in units of 1/min. [OSIPI code Q.PH1.008]
        ve (float):
            Relative volume fraction of the extracellular
            extravascular compartment (e). [OSIPI code Q.PH1.001.[e]]
        vp (float):
            Relative volyme fraction of the plasma compartment (p). [OSIPI code Q.PH1.001.[p]]
        Ta (float, optional):
            Arterial delay time, i.e., difference in onset time
            between tissue curve and AIF in units of sec.
            Defaults to 30 seconds. [OSIPI code Q.PH1.007]
        discretization_method (str, optional):
            Defines the discretization method. Options include

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
        - Adapted from contributions by: LEK_UoEdinburgh_UK, ST_USyd_AUS, MJT_UoEdinburgh_UK

    Example:

        Create an array of time points covering 6 min in steps of 1 sec,
        calculate the Parker AIF at these time points, calculate tissue concentrations
        using the Extended Tofts model and plot the results.

        Import packages:

        >>> import matplotlib.pyplot as plt
        >>> import osipi

        Calculate AIF

        >>> t = np.arange(0, 6 * 60, 0.1)
        >>> ca = osipi.aif_parker(t)

        Calculate tissue concentrations and plot

        >>> Ktrans = 0.6  # in units of 1/min
        >>> ve = 0.2  # takes values from 0 to 1
        >>> vp = 0.3  # takes values from 0 to 1
        >>> ct = osipi.extended_tofts(t, ca, Ktrans, ve, vp)
        >>> plt.plot(t, ca, "r", t, ct, "b")

    """
    # Input validation
    if t.size != ca.size:
        raise ValueError(f"t and ca must have the same size, got {t.size} and {ca.size}")

    for param, name in [(Ktrans, "Ktrans"), (ve, "ve"), (vp, "vp")]:
        if not (np.isscalar(param) and np.isreal(param)):
            raise TypeError(f"{name} must be a numeric scalar value, got {type(param).__name__}")

    if not (0 <= ve <= 1):
        raise ValueError(f"ve must be in range [0, 1], got {ve}")
    if not (0 <= vp <= 1):
        raise ValueError(f"vp must be in range [0, 1], got {vp}")
    if not (0 <= ve + vp <= 1):
        raise ValueError(f"Sum of ve ({ve}) and vp ({vp}) exceeds 1")
    if Ta < 0:
        raise ValueError(f"Ta must be non-negative, got {Ta}")
    if Ktrans < 0:
        raise ValueError(f"Ktrans must be non-negative, got {Ktrans}")

    if not np.allclose(np.diff(t), np.diff(t)[0]):
        warnings.warn(
            ("Non-uniform time spacing detected. Time array may be" " resampled."),
            stacklevel=2,
        )

    if Ktrans <= 0 or ve <= 0:
        ct = vp * ca

    else:
        # Convert units
        Ktrans = Ktrans / 60  # from 1/min to 1/sec

        if discretization_method == "exp":  # Use exponential convolution
            # Shift the AIF by the arterial delay time (if not zero)
            if Ta != 0:
                f = interp1d(
                    t,
                    ca,
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                ca = (t > Ta) * f(t - Ta)

            Tc = ve / Ktrans
            # expconv calculates convolution of ca and
            # (1/Tc)exp(-t/Tc), add vp*ca term for extended model
            ct = (vp * ca) + ve * exp_conv(Tc, t, ca)

        else:  # Use convolution by default
            # Calculate the impulse response function
            kep = Ktrans / ve
            imp = Ktrans * np.exp(-1 * kep * t)

            # Shift the AIF by the arterial delay time (if not zero)
            if Ta != 0:
                f = interp1d(
                    t,
                    ca,
                    kind="linear",
                    bounds_error=False,
                    fill_value=0,
                )
                ca = (t > Ta) * f(t - Ta)

            # Check if time data grid is uniformly spaced
            if np.allclose(np.diff(t), np.diff(t)[0]):
                # Convolve impulse response with AIF
                convolution = np.convolve(ca, imp)

                # Discard unwanted points, make sure time spacing is
                # correct and add vp*ca term for extended model
                ct = convolution[0 : len(t)] * t[1] + (vp * ca)
            else:
                # Resample at the smallest spacing
                dt = np.min(np.diff(t))
                t_resampled = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / dt))
                ca_func = interp1d(
                    t,
                    ca,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                imp_func = interp1d(
                    t,
                    imp,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                ca_resampled = ca_func(t_resampled)
                imp_resampled = imp_func(t_resampled)
                # Convolve impulse response with AIF
                convolution = np.convolve(ca_resampled, imp_resampled)

                # Discard unwanted points, make sure time spacing is
                # correct and add vp*ca term for extended model
                ct_resampled = convolution[0 : len(t_resampled)] * t_resampled[1] + (
                    vp * ca_resampled
                )

                # Restore time grid spacing
                ct_func = interp1d(
                    t_resampled,
                    ct_resampled,
                    kind="quadratic",
                    bounds_error=False,
                    fill_value=0,
                )
                ct = ct_func(t)

    return ct


def two_compartment_exchange_model(
    t: np.ndarray,
    ca: np.ndarray,
    Fp: float,
    PS: float,
    ve: float,
    vp: float,
    Ta: float = 30.0,
) -> np.ndarray:
    """Two compartment exchange model

    Tracer flows from the AIF to the blood plasma compartment; two-way leakage
    between the plasma and extracellular compartments(EES) is permitted.

    Args:
        t: 1D array of times(s). [OSIPI code is Q.GE1.004]
        ca: Arterial concentrations in mM for each time point in t. [OSIPI code is Q.IC1.001.[a]]
        Fp: Blood plasma flow rate into a unit tissue volume in ml/min. [OSIPI code is Q.PH1.002]
        PS: Permeability surface area product in ml/min. [OSIPI code is Q.PH1.004]
        ve: Extracellular volume fraction. [OSIPI code Q.PH1.001.[e]]
        vp: Plasma volume fraction. [OSIPI code Q.PH1.001.[p]]
        Ta: Arterial delay time, i.e.,
            difference in onset time between tissue curve and AIF in units of sec. [OSIPI code Q.PH1.007]

    Returns:
        Ct: Tissue concentrations in mM

    See Also:
        `extended_tofts`

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#indicator-kinetic-models
        - Lexicon code: M.IC1.009
        - OSIPI name: Two Compartment Exchange Model
        - Adapted from contributions by: MJT_UoEdinburgh_UK

    Example:
        Create an array of time points covering 6 min in steps of 1 sec,
        calculate the Parker AIF at these time points, calculate tissue concentrations
        using the Two Compartment Exchange model and plot the results.

        >>> import matplotlib.pyplot as plt
        >>> import osipi

        Calculate AIF

        >>> t = np.arange(0, 6 * 60, 0.1)
        >>> ca = osipi.aif_parker(t)

        Plot the tissue concentrations for an extracellular volume fraction
        of 0.2, plasma volume fraction of 0.1, permeability serface area of 5 ml/min
        and flow rate of 10 ml/min

        >>> PS = 5  # Permeability surface area product in ml/min
        >>> Fp = 10  # Flow rate in ml/min
        >>> ve = 0.2  # Extracellular volume fraction
        >>> vp = 0.1  # Plasma volume fraction
        >>> ct = osipi.two_compartment_exchange_model(t, ca, Fp, PS, ve, vp)
        >>> plt.plot(t, ca, "r", t, ct, "g")

    """
    # Input validation
    if t.size != ca.size:
        raise ValueError(f"t and ca must have the same size, got {t.size} and {ca.size}")

    for param, name in [(Fp, "Fp"), (PS, "PS"), (ve, "ve"), (vp, "vp")]:
        if not (np.isscalar(param) and np.isreal(param)):
            raise TypeError(f"{name} must be a numeric scalar value, got {type(param).__name__}")

    if Fp <= 0:
        raise ValueError(f"Fp must be positive, got {Fp}")
    if PS < 0:
        raise ValueError(f"PS must be non-negative, got {PS}")
    if not (0 <= ve <= 1):
        raise ValueError(f"ve must be in range [0, 1], got {ve}")
    if not (0 <= vp <= 1):
        raise ValueError(f"vp must be in range [0, 1], got {vp}")
    if not (0 <= ve + vp <= 1):
        raise ValueError(f"Sum of ve ({ve}) and vp ({vp}) exceeds 1")

    if vp == 0:
        E = 1 - np.exp(-PS / Fp)
        Ktrans = E * Fp
        return tofts(t, ca, Ktrans, ve, Ta, discretization_method="conv")

    if not np.allclose(np.diff(t), np.diff(t)[0]):
        warnings.warn(
            ("Non-uniform time spacing detected. Time array may be" " resampled."),
            stacklevel=2,
        )

    # Convert units
    fp_per_s = Fp / (60.0 * 100.0)
    ps_per_s = PS / (60.0 * 100.0)

    # Calculate the impulse response function
    v = ve + vp

    # Mean transit time
    T = v / fp_per_s
    tc = vp / fp_per_s
    te = ve / ps_per_s

    upsample_factor = 1
    n = t.size
    n_upsample = (n - 1) * upsample_factor + 1
    t_upsample = np.linspace(t[0], t[-1], n_upsample)
    tau_upsample = t_upsample - t[0]

    sig_p = ((T + te) + np.sqrt((T + te) ** 2 - 4 * tc * te)) / (2 * tc * te)
    sig_n = ((T + te) - np.sqrt((T + te) ** 2 - 4 * tc * te)) / (2 * tc * te)

    # Calculate the impulse response function for the plasma compartment and EES

    irf_cp = (
        vp
        * sig_p
        * sig_n
        * (
            (1 - te * sig_n) * np.exp(-tau_upsample * sig_n)
            + (te * sig_p - 1.0) * np.exp(-tau_upsample * sig_p)
        )
        / (sig_p - sig_n)
    )

    irf_ce = (
        ve
        * sig_p
        * sig_n
        * (np.exp(-tau_upsample * sig_n) - np.exp(-tau_upsample * sig_p))
        / (sig_p - sig_n)
    )

    irf_cp[[0]] /= 2
    irf_ce[[0]] /= 2

    dt = np.min(np.diff(t)) / upsample_factor

    if Ta != 0:
        f = interp1d(
            t,
            ca,
            kind="linear",
            bounds_error=False,
            fill_value=0,
        )
        ca = (t > Ta) * f(t - Ta)

    # get concentration in plasma and EES
    Cp = dt * convolve(ca, irf_cp, mode="full", method="auto")[: len(t)]
    Ce = dt * convolve(ca, irf_ce, mode="full", method="auto")[: len(t)]

    t_upsample = np.linspace(t[0], t[-1], n_upsample)

    Cp = np.interp(t, t_upsample, Cp)
    Ce = np.interp(t, t_upsample, Ce)

    # get tissue concentration
    Ct = Cp + Ce
    return Ct
