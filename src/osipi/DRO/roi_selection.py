import numpy as np
from matplotlib import path
from matplotlib import pyplot as plt
from matplotlib.widgets import LassoSelector


def roi(signal, slice_num):
    """
    Select a region of interest (ROI) in a slice of a 4D signal.
    """

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.set_title("Slice:")
    ax1.imshow(signal[:, :, slice_num, 0], cmap="gray", interpolation="nearest")

    # Empty array to be filled with lasso selector
    array = np.zeros_like(signal[:, :, slice_num, 0])
    ax2 = fig.add_subplot(122)
    ax2.set_title("numpy array:")
    mask = ax2.imshow(array, vmax=1, interpolation="nearest")

    plt.show()
    # Pixel coordinates
    pix = np.arange(signal.shape[1])
    xv, yv = np.meshgrid(pix, pix)
    pix = np.vstack((xv.flatten(), yv.flatten())).T

    def updateArray(array, indices):
        lin = np.arange(array.size)
        newArray = array.flatten()
        newArray[lin[indices]] = 1
        return newArray.reshape(array.shape)

    def onselect(verts):
        array = mask._A._data
        p = path.Path(verts)
        ind = p.contains_points(pix, radius=1)
        array = updateArray(array, ind)
        mask.set_data(array)
        fig.canvas.draw_idle()

    lineprops = {"color": "red", "linewidth": 4, "alpha": 0.8}
    lasso = LassoSelector(ax1, onselect, lineprops, button=1)
    mask_4d = np.zeros(signal.shape)
    mask_4d[:, :, slice_num, :] = mask

    return lasso, mask_4d
