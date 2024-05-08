import numpy as np
import osipi


def test_signal_R1_to_s_linear():

    # 1. Simple use case
    R_1 = np.array([0.0, 1.5, 3.0, 4.0, 10.0], dtype=np.float64)  # R1 in units of /s
    k = np.float64(150.0)  # constant of proportionality in units of arb. unit s
    S_truth = np.array([0.0, 225.0, 450.0, 600.0, 1500.0])  # expected signal in arb. unit
    S = osipi.R1_to_S_linear(R_1, k)  # estimated signal
    np.testing.assert_allclose(S_truth, S, rtol=0, atol=1e-7)


def test_signal_R1_to_S_SPGR_model():

    # 1. Simple use case
    # test data created using https://github.com/mjt320/SEPAL
    R_1 = np.array([0.1, 0.2, 0.5, 1, 2, 10, 50], dtype=np.float64)
    S_0 = np.float64(100)
    TR = np.float64(5e-3)
    a = np.float64(15)
    S_truth = np.array([0.37438758,  0.73827771,  1.77119982,  3.31912401,  5.89510144, 15.5485315, 23.10948814], dtype=np.float64)
    S = osipi.R1_to_S_SPGR_model(R_1, S_0, TR, a)
    np.testing.assert_allclose(S_truth, S, rtol=0, atol=1e-7)


if __name__ == "__main__":

    test_signal_R1_to_s_linear()
    test_signal_R1_to_S_SPGR_model()

    print('All signal functionality tests passed!!')
