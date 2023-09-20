import numpy as np
import osipi


def test_tofts():

    t = np.arange(0, 6*60, 1)
    ca = osipi.aif_parker(t)
    ct = osipi.tofts(t, ca, Ktrans=0.6, ve=0.2)

    # Test that the peak tissue concentration is less than the peak AIF
    assert np.round(np.max(ct)) < np.round(np.max(ca))


if __name__ == "__main__":

    test_tofts()

    print('All Tofts model tests passed!!')

