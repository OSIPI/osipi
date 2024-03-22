import numpy as np
from scipy.interpolate import interp1d
from ._convolution import exp_conv
import warnings


def R1_to_s_linear(R1: float, k:float) -> float:
    """Linear model for relationship between R1 and magnitude signal, s = k.R1

    Args:
        R1 (float): longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        k (float): proportionality constant in units of arb. unit s [OSIPI code Q.GE1.009]

    Returns:
        float: magnitude signal in arb. unit [OSIPI code Q.MS1.001]

        References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#LinModel_SM2
        - Lexicon code: M.SM2.001
        - OSIPI name: Linear model
        - Adapted from equation given in the Lexicon

    Example:

        Convert a single R1 value to the corresponding signal intensity.

        Import packages:

        >>> import osipi

        Calculate signal:

        >>> R1 = 3.0  # R1 in units of /s
        >>> k = 150.0  # constant of proportionality in units of arb. unit s
        >>> s = osipi.R1_to_s_linear(R1, k)
        >>> print(s)
    """
    # calculate signal
    return k*R1
