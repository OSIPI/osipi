import numpy as np
from numpy.typing import NDArray


# Use a more generic floating-point type annotation
def signal_linear(R1: NDArray[np.floating], k: np.floating) -> NDArray[np.floating]:
    """Linear model for relationship between R1 and magnitude signal
    Args:
        R1 (NDArray[np.floating]): longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        k (np.floating): proportionality constant in a.u. S [OSIPI code Q.GE1.009]
    Returns:
        NDArray[np.floating]: magnitude signal in a.u. [OSIPI code Q.MS1.001]
    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#LinModel_SM2
        - Lexicon code: M.SM2.001
        - OSIPI name: Linear model
        - Adapted from equation given in the Lexicon
    """
    # calculate signal
    return k * R1  # S


def signal_SPGR(
    R1: NDArray[np.floating],
    S0: NDArray[np.floating],
    TR: np.floating,
    a: np.floating,
) -> NDArray[np.floating]:
    """Steady-state signal for SPGR sequence.
    Args:
        R1 (NDArray[np.floating]): longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        S0 (NDArray[np.floating]): fully T1-relaxed signal in a.u. [OSIPI code Q.MS1.010]
        TR (np.floating): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.floating): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]
    Returns:
        NDArray[np.floating]: magnitude signal in a.u. [OSIPI code Q.MS1.001]
    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#SPGR%20model
        - Lexicon code: M.SM2.002
        - OSIPI name: Spoiled gradient recalled echo model
        - Adapted from equation given in the Lexicon and contribution from MJT_UoEdinburgh_UK
    """
    # calculate signal
    a_rad = a * np.pi / 180
    exp_TR_R1 = np.exp(-TR * R1)
    return S0 * (((1.0 - exp_TR_R1) * np.sin(a_rad)) / (1.0 - exp_TR_R1 * np.cos(a_rad)))  # S
