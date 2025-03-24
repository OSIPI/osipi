import numpy as np
from numpy.typing import NDArray


def exp_conv(
    T: np.floating, t: NDArray[np.floating], a: NDArray[np.floating]
) -> NDArray[np.floating]:
    """Exponential convolution operation of (1/T)exp(-t/T) with a.

    Args:
        T (np.floating): exponent in time units
        t (NDArray[np.floating]): array of time points
        a (NDArray[np.floating]): array to be convolved with time exponential

    Returns:
        NDArray[np.floating]: convolved array
    """
    if T == 0:
        return a

    n = len(t)
    f = np.zeros((n,))

    x = (t[1 : n - 1] - t[0 : n - 2]) / T
    da = (a[1 : n - 1] - a[0 : n - 2]) / x

    E = np.exp(-x)
    E0 = 1 - E
    E1 = x - E0

    add = a[0 : n - 2] * E0 + da * E1

    for i in range(0, n - 2):
        f[i + 1] = E[i] * f[i] + add[i]

    f[n - 1] = f[n - 2]
    return f
