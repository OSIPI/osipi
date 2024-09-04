import os

import numpy as np
import pydicom

from osipi.DRO._filters_and_noise import median_filter


def read_dicom_slices_as_4d_signal(folder_path):
    """
    Read a DICOM series from a folder path.
    Returns the signal data as a 4D numpy array (x, y, z, t).
    """
    slices = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".dcm"):
                dicom_file = os.path.join(root, file)
                slice = pydicom.read_file(dicom_file)
                if slice.SliceLocation not in slices:
                    slices[slice.SliceLocation] = []
                slices[slice.SliceLocation].append((slice.AcquisitionTime, slice))

    # Sort each list of slices by the first element (AcquisitionTime)
    for slice_location in slices:
        slices[slice_location].sort(key=lambda x: x[0])

    spatial_shape = slices[slice_location][0][1].pixel_array.shape

    data_shape = (spatial_shape[0], spatial_shape[1], len(slices), len(slices[slice_location]))

    signal = np.zeros(data_shape)

    for z, slice_location in enumerate(sorted(slices.keys())):  # Sort by slice location
        slices[z] = slices.pop(slice_location)
        for t, (_, slice) in enumerate(
            sorted(slices[z], key=lambda x: x[0])
        ):  # Sort by acquisition time
            signal[:, :, z, t] = slice.pixel_array
            slices[z][t] = slice

    return signal, slices, slices[0][0]


def signal_enhancement_extract(S, datashape, baselinepoints):
    # Take baseline average
    S0 = np.average(S[:, :, :, 0:baselinepoints], axis=3)  # Take baseline signal
    E = np.zeros_like(S)

    # Calcualte siganl enhancement
    for i in range(0, datashape[-1]):
        E[:, :, :, i] = S[:, :, :, i] - S0
        E[:, :, :, i] = median_filter(E[:, :, :, i])  # Median filter size (3,3)

    return E, S0, S
