
Generating an AIF
^^^^^^^^^^^^^^^^^

Generate an AIF and plot it:

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import osipi.dc.models.concentration.aif as aif

    t = np.arange(0, 6*60, 1)
    ca = aif.parker(t)
    plt.plot(t, ca)
    plt.show()


Generating a tissue concentration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coming soon..


Generating an MRI signal
^^^^^^^^^^^^^^^^^^^^^^^^

Coming soon..


Adding measurement error
^^^^^^^^^^^^^^^^^^^^^^^^

Coming soon..


