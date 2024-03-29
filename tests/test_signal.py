import numpy as np
import osipi


def test_signal_R1_to_s_linear():

    # 1. Simple use case
    R1 = np.array([0.0, 1.5, 3.0, 4.0, 10.0])  # R1 in units of /s
    k = np.float64(150.0)  # constant of proportionality in units of arb. unit s
    signal_truth = np.array([0.0, 225.0, 450.0, 600.0, 1500.0])  # expected signal in arb. unit
    signal = osipi.R1_to_s_linear(R1, k)  # estimated signal
    np.testing.assert_allclose(signal_truth, signal, rtol=0, atol=1e-7)


if __name__ == "__main__":

    test_signal_R1_to_s_linear()

    print('All signal functionality tests passed!!')

