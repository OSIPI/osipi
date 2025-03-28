from typing import Union

import numpy as np
from numpy.typing import NDArray


def signal_linear(
    R1: Union[np.float64, NDArray[np.float64]], k: Union[np.float64, NDArray[np.float64]]
) -> Union[np.float64, NDArray[np.float64]]:
    """
    Linear model for the relationship between R1 and magnitude signal.

    Args:
        R1 (Union[np.float64, NDArray[np.float64]]): Longitudinal relaxation rate in units of /s.
        k (Union[np.float64, NDArray[np.float64]]): Proportionality constant in arbitrary units.

    Returns:
        Union[np.float64, NDArray[np.float64]]: Magnitude signal in arbitrary units.
    """
    return k * R1


def signal_SPGR(
    R1: Union[np.float64, NDArray[np.float64]],
    S0: Union[np.float64, NDArray[np.float64]],
    TR: Union[np.float64, NDArray[np.float64]],
    a: Union[np.float64, NDArray[np.float64]],
) -> Union[np.float64, NDArray[np.float64]]:
    """
    Steady-state signal for SPGR sequence.

    Args:
        R1 (Union[np.float64, NDArray[np.float64]]): Longitudinal relaxation rate in units of /s.
        S0 (Union[np.float64, NDArray[np.float64]]): Fully T1-relaxed signal in arbitrary units.
        TR (Union[np.float64, NDArray[np.float64]]): Repetition time in seconds.
        a (Union[np.float64, NDArray[np.float64]]): Prescribed flip angle in degrees.

    Returns:
        Union[np.float64, NDArray[np.float64]]: Magnitude signal in arbitrary units.
    """
    a_rad = a * np.pi / 180  # Convert degrees to radians
    exp_TR_R1 = np.exp(-TR * R1)
    return S0 * (((1.0 - exp_TR_R1) * np.sin(a_rad)) / (1.0 - exp_TR_R1 * np.cos(a_rad)))
