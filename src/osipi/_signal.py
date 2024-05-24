import numpy as np
from numpy.typing import NDArray


def R1_to_S_linear(R_1: NDArray[np.float64], k: np.float64) -> NDArray[np.float64]:
    """Linear model for relationship between R_1 and magnitude signal, S = k.R_1

    Args:
        R_1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        k (np.float64): proportionality constant in units of a.u. S [OSIPI code Q.GE1.009]

    Returns:
        1D array of floats: vector of magnitude signal in a.u. [OSIPI code Q.MS1.001]

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#LinModel_SM2
        - Lexicon code: M.SM2.001
        - OSIPI name: Linear model
        - Adapted from equation given in the Lexicon
    """
    # check R_1 is a 1D array of floats
    if not (isinstance(R_1, np.ndarray) and R_1.ndim == 1 and R_1.dtype == np.float64):
        raise TypeError("R_1 must be a 1D NumPy array of np.float64")
    # calculate signal
    return k*R_1  # S


def R1_to_S_SPGR_model(R_1: NDArray[np.float64], S_0: np.float64, TR: np.float64, a: np.float64) -> NDArray[np.float64]:
    """Convert R_1 to steady-state signal for SPGR sequence.

    Args:
        R_1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        S_0 (np.float64): fully T1-relaxed signal in units of a.u.. [OSIPI code Q.MS1.010]
        TR (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]

    Returns:
        1D array of np.float64: vector of magnitude signal in a.u. [OSIPI code Q.MS1.001]

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#SPGR%20model
        - Lexicon code: M.SM2.002
        - OSIPI name: Spoiled gradient recalled echo model
        - Adapted from equation given in the Lexicon and contribution from MJT_UoEdinburgh_UK
    """
    # check R_1 is a 1D array of floats
    if not (isinstance(R_1, np.ndarray) and R_1.ndim == 1 and R_1.dtype == np.float64):
        raise TypeError("R_1 must be a 1D NumPy array of np.float64")
    # calculate signal
    a_rad = a * np.pi / 180
    exp_TR_R1 = np.exp(-TR*R_1)
    return S_0 * (((1. - exp_TR_R1) * np.sin(a_rad)) / (1. - exp_TR_R1 * np.cos(a_rad)))  # S
