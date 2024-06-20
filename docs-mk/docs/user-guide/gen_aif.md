

## Generate an AIF and plot it:
```  py
import numpy as np
import matplotlib.pyplot as plt
import osipi

t = np.arange(0, 6*60, 1)
ca = osipi.aif_parker(t)
plt.plot(t, ca)
plt.show()
```

## Generating a tissue concentration

``` py
import numpy as np
import matplotlib.pyplot as plt
import osipi

t = np.arange(0, 6*60, 1)
ca = osipi.aif_parker(t)
Ktrans = 0.6
ve = 0.2
ct = osipi.tofts(t, ca, Ktrans=Ktrans/60, ve=ve)
plt.plot(t, ct)
plt.show()
```

## Generating an MRI signal
!!! note "Coming Soon"
    This section is under development and will be available soon.

## Adding measurement error
!!! note "Coming Soon"
    This section is under development and will be available soon.
