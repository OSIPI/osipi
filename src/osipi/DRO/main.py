import numpy as np
from DICOM_processing import (
    calc_concentration,
    calculate_baseline,
    read_dicom_slices_as_signal,
    signal_to_R1,
)
from Display import animate_mri
from roi_selection import roi

slices, dicom_ref = read_dicom_slices_as_signal("data/subject1/13.000000-perfusion-23726")
anim = animate_mri(slices, mode="time", slice_index=7, time_index=5)
TR = 1e-3 * dicom_ref.RepetitionTime
TE = 1e-3 * dicom_ref.EchoTime
flip_angle = dicom_ref.FlipAngle
baseline = 5
R10 = 1.18
r1 = 3.9

baseline_signal = calculate_baseline(slices, baseline)
R1 = signal_to_R1(slices, baseline_signal, TR)
c_tissue = calc_concentration(R1, R10, r1)

Max = np.max(c_tissue, axis=-1, keepdims=True)
mask, roi_sum, lasso = roi(Max, 5, c_tissue.shape, save=True)
