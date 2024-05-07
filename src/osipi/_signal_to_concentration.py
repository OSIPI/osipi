import numpy as np
from numpy.typing import NDArray


def s_to_C_via_ep_SPGR(s: NDArray[np.float64], s_pre: np.float64, R10: np.float64, tr: np.float64, a: np.float64, r1: np.float64) -> NDArray[np.float64]:
    """Signal to concentration via electromagnetic property (SPGR, FXL, analytical linear relaxivity)
    Args:
        s (1D array of np.float64): vector of magnitude signals in arb. unit [OSIPI code Q.MS1.001]
        s_pre (np.float64): pre-contrast magnitude signal in arb. unit [OSIPI code Q.MS1.001]
        R10 (np.float64): native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        tr (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]
        r1 (np.float64): longitudinal relaxivity in units of /s/mM. [OSIPI code Q.EL1.015]

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
    return C


def s_to_ep_SPGR(s: NDArray[np.float64], s_pre: np.float64, R10: np.float64, tr: np.float64, a: np.float64) -> NDArray[np.float64]:
    """Signal to electromagnetic property conversion (analytical, SPGR, FXL)
    Args:
        s (1D array of np.float64): vector of magnitude signals in arb. unit [OSIPI code Q.MS1.001]
        s_pre (np.float64): pre-contrast magnitude signal in arb. unit [OSIPI code Q.MS1.001]
        R10 (np.float64): native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        tr (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]

    Returns:
        1D array of np.float64: vector of R1 in units of /s. [OSIPI code Q.EL1.001]

    References/notes:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#
        - Lexicon code: P.SE1.001
        - OSIPI name: model-based
        - Inversion method: analytical inversion [OSIPI code G.MI1.001]
        - Forward model: Spoiled gradient recalled echo model [OSIPI code M.SM2.002]
        - Adapted from contribution of LEK_UoEdinburgh_UK
    """
    # check s is a 1D array of floats
    if not (isinstance(s, np.ndarray) and s.ndim == 1 and s.dtype == np.float64):
        raise TypeError("s must be a 1D NumPy array of np.float64")
    a_rad = a * np.pi / 180
    # estimate fully T1-relaxed signal in units of arb. unit. [OSIPI code Q.MS1.010]
    exp_tr_R10 = np.exp(-tr*R10)
    sin_a = np.sin(a_rad)
    cos_a = np.cos(a_rad)
    s0 = s_pre * (1 - cos_a * exp_tr_R10) / (sin_a * (1 - exp_tr_R10))
    return np.log(((s0*sin_a)-s)/(s0*sin_a-(s*cos_a)))*(-1/tr)


def ep_to_c(R1: NDArray[np.float64], R10: np.float64, r1: np.float64):
    """Electromagnetic property inverse model: longitudinal relaxation rate, linear with relaxivity
    Args:
        R1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        R10 (np.float64): native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        r1 (np.float64): longitudinal relaxivity in units of /s/mM. [OSIPI code Q.EL1.015]

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
    # check R1 is a 1D array of floats
    if not (isinstance(R1, np.ndarray) and R1.ndim == 1 and R1.dtype == np.float64):
        raise TypeError("R1 must be a 1D NumPy array of np.float64")
    return (R1 - R10) / r1

def R1_to_s_SPGR_model(R1: NDArray[np.float64], s0: np.float64, tr: np.float64, a: np.float64) -> NDArray[np.float64]:
    """Magnitude models: DCE - R1 in the fast water exchange limit (SPGR)

    Args:
        R1 (1D array of np.float64): vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        s0 (np.float64): fully T1-relaxed signal in units of arb. unit. [OSIPI code Q.MS1.010]
        tr (np.float64): repetition time in units of s. [OSIPI code Q.MS1.006]
        a (np.float64): prescribed flip angle in units of deg. [OSIPI code Q.MS1.007]

    Returns:
        1D array of np.float64: vector of magnitude signals in arb. unit [OSIPI code Q.MS1.001]

    References:
        - Lexicon url: https://osipi.github.io/OSIPI_CAPLEX/perfusionModels/#SPGR%20model
        - Lexicon code: M.SM2.002
        - OSIPI name: Spoiled gradient recalled echo model
        - Adapted from equation given in the Lexicon and contribution from MJT_UoEdinburgh_UK
    """
    # check R1 is a 1D array of floats
    if not (isinstance(R1, np.ndarray) and R1.ndim == 1 and R1.dtype == np.float64):
        raise TypeError("R1 must be a 1D NumPy array of np.float64")
    # calculate signal
    a_rad = a * np.pi / 180
    return s0 * (((1.-np.exp(-tr*R1))*np.sin(a_rad)) / (1.-np.exp(-tr*R1)*np.cos(a_rad)))
