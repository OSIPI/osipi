import numpy as np
from numpy.typing import NDArray


def R1_to_s_linear(R1: NDArray[np.float64], k: np.float64) -> NDArray[np.float64]:
    """Linear model for relationship between R1 and magnitude signal, s = k.R1

    Args:
        R1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        k (np.float64): proportionality constant in units of arb. unit s [OSIPI code Q.GE1.009]

    Returns:
        1D array of floats: vector of magnitude signal in arb. unit [OSIPI code Q.MS1.001]

        References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#LinModel_SM2
        - Lexicon code: M.SM2.001
        - OSIPI name: Linear model
        - Adapted from equation given in the Lexicon
    """
    # check R1 is a 1D array of floats
    if not (isinstance(R1, np.ndarray) and R1.ndim == 1 and R1.dtype == np.float64):
        raise TypeError("R1 must be a 1D NumPy array of np.float64")
    # calculate signal
    return k*R1


