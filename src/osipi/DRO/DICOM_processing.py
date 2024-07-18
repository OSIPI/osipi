import os

import numpy as np
import pydicom


def read_dicom_slices_as_signal(folder_path):
    """
    Read a DICOM series from a folder path.
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

    data_shape = (spatial_shape, spatial_shape, len(slices), len(slices[slice_location]))

    signal = np.zeros(data_shape)

    for z, slice_location in enumerate(sorted(slices.keys())):  # Sort by slice location
        for t, (_, slice) in enumerate(
            sorted(slices[slice_location], key=lambda x: x[0])
        ):  # Sort by acquisition time
            signal[:, :, z, t] = slice.pixel_array

    return signal


def signal_enhanecment(signal, baseline=0):
    """
    Calculate signal enhancement.
    """
    s0 = np.average(signal[:, :, :, :baseline], axis=-1)
    return (signal - s0) / s0, s0
