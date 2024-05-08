import numpy as np
import osipi


def test_signal_to_concentration_S_to_C_via_ep_SPGR():

    # 1. Simple use case
    # Test data and ground truth adapted from OSIPI repository tests ("vox_1")
    S = np.array(
        [7, 9, 6, 10, 9, 6, 9, 10, 9, 9, 9, 12, 8, 10, 12, 15, 53, 70, 71, 70, 63, 58, 54, 50, 53, 48, 52, 49, 42],
        dtype=np.float64)
    S_BL = np.mean(S[:1])  # average first two points for baseline signal
    R_10 = np.float64(1 / 1.4)
    TR = np.float64(0.002)
    a = np.float64(13)
    r_1 = np.float64(4.5)

    C = osipi.S_to_C_via_ep_SPGR(S, S_BL, R_10, TR, a, r_1)
    C_truth = np.array(
        [5.896517841898054e-15, 0.04861114658132921, -0.02373686966428807, 0.0735037381246513, 0.04861114658132921,
         -0.02373686966428807, 0.04861114658132921, 0.0735037381246513, 0.04861114658132921, 0.04861114658132921,
         0.04861114658132921, 0.12451099240893969, 0.02411300135228399, 0.0735037381246513, 0.12451099240893969,
         0.2042308274298612, 1.723816850668738, 2.9860012006598615, 3.0813949356951134, 2.9860012006598615,
         2.3932805439961378, 2.0365845677672656, 1.7832505654332091, 1.5539858164348437, 1.723816850668738,
         1.4473321937838983, 1.6658291725704821, 1.5000331327922662, 1.15513218792702], dtype=np.float64)
    np.testing.assert_allclose(C_truth, C, rtol=0, atol=1e-7)


def test_signal_to_concentration_S_to_ep_SPGR():

    # 1. Simple use case
    # test data created using https://github.com/mjt320/SEPAL
    return


def test_signal_to_concentration_ep_to_C_R1_lin_rxy():
    return


if __name__ == "__main__":

    test_signal_to_concentration_S_to_C_via_ep_SPGR()
    #test_signal_to_concentration_S_to_ep_SPGR()
    #test_signal_to_concentration_ep_to_C_R1_lin_rxy()

    print('All signal functionality tests passed!!')
