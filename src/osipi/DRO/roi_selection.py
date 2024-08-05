import numpy as np
from matplotlib import path
from matplotlib import pyplot as plt
from matplotlib.widgets import LassoSelector


def roi(signal, slice_num, data_shape, save=False):
    """
    Select a region of interest (ROI) in a slice of a 4D signal.
    """

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.set_title("Slice:")
    ax1.imshow(signal[:, :, slice_num], cmap="gray", interpolation="nearest")

    # Empty array to be filled with lasso selector
    array = np.zeros_like(signal[:, :, slice_num])
    ax2 = fig.add_subplot(122)
    ax2.set_title("numpy array:")
    mask = ax2.imshow(array, vmax=1, interpolation="nearest")

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

    lasso = LassoSelector(ax1, onselect, button=1)
    plt.show()
    mask2d = mask._A._data.copy()
    roivox = np.sum(mask2d)
    timemask = np.tile(mask2d[:, :, np.newaxis], (1, 1, signal.shape[-1]))
    mask4d = np.zeros(data_shape)
    mask4d[:, :, slice_num, :] = timemask
    if save:
        np.save("ROI_saved/aif_mask.npy", mask4d)
        np.save("ROI_saved/roi_voxels.npy", roivox)
    return mask4d, roivox, lasso


def ICfromROI(E, mask, roivox, numaxis):
    Eroi = (
        np.sum(mask * E, axis=tuple(range(0, numaxis)))
    ) / roivox  # calculates average roi signal enhancement

    return Eroi
