

## Generate an AIF and plot it:
```  py
import numpy as np
import matplotlib.pyplot as plt
import osipi

t = np.arange(0, 6*60, 1)
ca = osipi.aif_parker(t)
plt.plot(t, ca)
plt.xlabel('Time (s)')
plt.ylabel('Indicator concentration (mM)')
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
fig, ax = plt.subplots(1, 2)
ax[0].plot(t, ca)
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Indicator concentration (mM)')
ax[0].set_title('AIF')
ax[1].plot(t, ct)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Indicator concentration (mM)')
ax[1].set_title('Tissue')

fig.tight_layout()
plt.show()
```

## Generating an MRI signal

``` py
import numpy as np
import matplotlib.pyplot as plt
import osipi

t = np.arange(0, 6*60, 1)
ca = osipi.aif_parker(t)
Ktrans = 0.6
ve = 0.2
ct = osipi.tofts(t, ca, Ktrans=Ktrans/60, ve=ve)

R10 = 0.5
r1 = 4.5
R1t = osipi.C_to_R1_linear_relaxivity(ct, R10, r1)

S0 = 1
TR = 0.004
a = 12
St = osipi.signal_SPGR(R1t, S0, TR, a)

fig, ax = plt.subplots(1, 2)
ax[0].plot(t, ct)
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Indicator concentration (mM)')
ax[0].set_title('Concentration')
ax[1].plot(t, St)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('MRI signal (a.u)')
ax[1].set_title('MRI signal')

fig.tight_layout()
plt.show()
```

## Adding measurement error
!!! note "Coming Soon"
    This section is under development and will be available soon.
