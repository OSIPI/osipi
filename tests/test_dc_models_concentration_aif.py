import numpy as np
import osipi.dc.models.concentration.aif as aif

def test_parker():
    t = np.arange(0, 6*60, 1)
    ca = aif.parker(t)
    assert np.round(np.amax(ca)) == 6

if __name__ == "__main__":
    test_parker()
    print('All AIF tests passed')