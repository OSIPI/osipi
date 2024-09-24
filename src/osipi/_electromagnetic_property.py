import numpy as np
from numpy.typing import NDArray


def R1_to_C_linear_relaxivity(
    R1: NDArray[np.float64], R10: np.float64, r1: np.float64
) -> NDArray[np.float64]:
    """
    Electromagnetic property inverse model:
    - longitudinal relaxation rate, linear with relaxivity

    Converts R1 to tissue concentration

    Args:
        R1 (1D array of np.float64):
            Vector of longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.001]
        R10 (np.float64):
            Native longitudinal relaxation rate in units of /s. [OSIPI code Q.EL1.002]
        r1 (np.float64):
            Longitudinal relaxivity in units of /s/mM. [OSIPI code Q.EL1.015]

    Returns:
        NDArray[np.float64]:
            Vector of indicator concentration in units of mM. [OSIPI code Q.IC1.001]

    References:
        - Lexicon URL: https://osipi.github.io/OSIPI_CAPLEX/perfusionProcesses/#
        - Lexicon code: P.EC1.001
        - OSIPI name: model-based
          - Inversion method: analytical inversion [OSIPI code G.MI1.001]
          - Forward model:
            longitudinal relaxation rate, linear with relaxivity model [OSIPI code M.EL1.003]
        - Adapted from equation given in lexicon
    """
    # Check R1 is a 1D array of floats
    if not (isinstance(R1, np.ndarray) and R1.ndim == 1 and R1.dtype == np.float64):
        raise TypeError("R1 must be a 1D NumPy array of np.float64")
    elif not (r1 >= 0):
        raise ValueError("r1 must be positive")
    return (R1 - R10) / r1  # C
