import numpy as np
from numpy.typing import NDArray


def S_to_C_via_ep_SPGR(S: NDArray[np.float64], S_BL: np.float64, R_10: np.float64, TR: np.float64, a: np.float64, r_1: np.float64) -> NDArray[np.float64]:
    """Signal to concentration via electromagnetic property (SPGR, FXL, analytical linear R_1 relaxivity)

    Converts S -> R_1 -> C

    Args:
        S (1D array of np.float64): vector of magnitude signals in a.u. [OSIPI code Q.MS1.001]
        S_BL (np.float64): pre-contrast magnitude signal in a.u. [OSIPI code Q.MS1.001]
        R_10 (np.float64): native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        TR (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]
        r_1 (np.float64): longitudinal relaxivity in units of /s/mM. [OSIPI code Q.EL1.015]

    Returns:
        1D array of np.float64: vector of indicator total (across all compartments) indicator concentration in units of mM. [OSIPI code Q.IC1.001]

    References/notes:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#
        - Lexicon code: P.SC2.002
        - OSIPI name: ConvertSToCViaEP
        - Signal to electromagnetic property conversion method: model-based [P.SE1.001]
            - Inversion method: analytical inversion [OSIPI code G.MI1.001]
            - Forward model: Spoiled gradient recalled echo model [OSIPI code M.SM2.002]
        - Electromagnetic property inverse model: model-based [P.EC1.001]
            - Inversion method: analytical inversion [OSIPI code G.MI1.001]
            - Forward model: longitudinal relaxation rate, linear with relaxivity model [M.EL1.003]
    """
    R_1 = S_to_ep_SPGR(S, S_BL, R_10, TR, a)  # S -> R_1
    return ep_to_C_R1_lin_rxy(R_1, R_10, r_1)  # R1 -> C


def S_to_ep_SPGR(S: NDArray[np.float64], S_BL: np.float64, R_10: np.float64, TR: np.float64, a: np.float64) -> NDArray[np.float64]:
    """Signal to electromagnetic property conversion (analytical, SPGR, FXL)

    Converts Signal to R_1

    Args:
        S (1D array of np.float64): vector of magnitude signals in a.u. [OSIPI code Q.MS1.001]
        S_BL (np.float64): pre-contrast magnitude signal in a.u. [OSIPI code Q.MS1.001]
        R_10 (np.float64): native longitudinal relaxation rate in units of /S. [OSIPI code Q.EL1.002]
        TR (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]

    Returns:
        1D array of np.float64: vector of R_1 in units of /s. [OSIPI code Q.EL1.001]

    References/notes:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#
        - Lexicon code: P.SE1.001
        - OSIPI name: model-based
            - Inversion method: analytical inversion [OSIPI code G.MI1.001]
            - Forward model: Spoiled gradient recalled echo model [OSIPI code M.SM2.002]
        - Adapted from contribution of LEK_UoEdinburgh_UK
    """
    # check S is a 1D array of floats
    if not (isinstance(S, np.ndarray) and S.ndim == 1 and S.dtype == np.float64):
        raise TypeError("S must be a 1D NumPy array of np.float64")
    a_rad = a * np.pi / 180
    # estimate fully T1-relaxed signal S_0 in units of a.u.. [OSIPI code Q.MS1.010], then R_1
    exp_TR_R10 = np.exp(-TR*R_10)
    sin_a = np.sin(a_rad)
    cos_a = np.cos(a_rad)
    S_0 = S_BL * (1 - cos_a * exp_TR_R10) / (sin_a * (1 - exp_TR_R10))
    return np.log(((S_0*sin_a)-S)/(S_0*sin_a-(S*cos_a)))*(-1/TR)  # R_1


def ep_to_C_R1_lin_rxy(R_1: NDArray[np.float64], R_10: np.float64, r_1: np.float64):
    """Electromagnetic property inverse model: longitudinal relaxation rate, linear with relaxivity

    Converts R_1 to tissue concentration

    Args:
        R_1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        R_10 (np.float64): native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        r_1 (np.float64): longitudinal relaxivity in units of /s/mM. [OSIPI code Q.EL1.015]

    Returns:
        1D array of np.float64: vector of indicator concentration in units of mM. [OSIPI code Q.IC1.001]

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#
        - Lexicon code: P.EC1.001
        - OSIPI name: model-based
        - Inversion method: analytical inversion [OSIPI code G.MI1.001]
        - Forward model: longitudinal relaxation rate, linear with relaxivity model [M.EL1.003]
        - Adapted from equation given in lexicon
    """
    # check R_1 is a 1D array of floats
    if not (isinstance(R_1, np.ndarray) and R_1.ndim == 1 and R_1.dtype == np.float64):
        raise TypeError("R_1 must be a 1D NumPy array of np.float64")
    return (R_1 - R_10) / r_1  # C

