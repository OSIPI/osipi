import time

import numpy as np
from DICOM_processing import (
    SignalEnhancementExtract,
    read_dicom_slices_as_4d_signal,
)
from Display import animate_mri
from matplotlib import pyplot as plt
from roi_selection import ICfromROI

import osipi
from osipi.DRO.Conc2DROSignal import Conc2Sig_Linear, STDmap, addnoise, calcR1_R2, createR10_withref
from osipi.DRO.filters_and_noise import median_filter
from osipi.DRO.Model import (
    ForwardsModTofts,
    extended_tofts_model_1vox,
    modifiedToftsMurase,
    modifiedToftsMurase1Vox,
)

signal, slices, dicom_ref = read_dicom_slices_as_4d_signal(
    "data/subject2/12.000000-perfusion-17557"
)
# anim = animate_mri(slices, mode="time", slice_index=7, time_index=5)
data_shape = signal.shape

E, S0, S = SignalEnhancementExtract(signal, data_shape, 5)

Max = np.max(E, axis=-1, keepdims=True)

dt = 4.8 / 60  # mins from the RIDER website DCE description
t = np.linspace(0, dt * S.shape[-1], S.shape[-1])  # time series points

aif_dir = "ROI_saved/"

aifmask = np.load("{}aifmask.npy".format(aif_dir))
sagmask = np.load("{}sagmask.npy".format(aif_dir))
roivoxa = np.load("{}aifmaskvox.npy".format(aif_dir))
roivoxv = np.load("{}sagmaskvox.npy".format(aif_dir))

z = 5

Ea = ICfromROI(E, aifmask, roivoxa, aifmask.ndim - 1)
Ev = ICfromROI(E, sagmask, roivoxv, sagmask.ndim - 1)
S0ref = ICfromROI(S0[:, :, z], sagmask[:, :, z, 0], roivoxv, sagmask.ndim - 2)

max_index = np.unravel_index(np.argmax(E * aifmask, axis=None), E.shape)
print(max_index)

Hct = 0.45

E_vox = E[max_index[0], max_index[1], max_index[2], :]

start_time = time.time()

k1, ve, vp = extended_tofts_model_1vox(Ea, E_vox, t)

end_time = time.time()

execution_time = end_time - start_time

print(f"The execution time of the line is: {execution_time} seconds")

K1, K2, Vp = modifiedToftsMurase(Ea / (1 - Hct), E, dt, data_shape)

k1_vox = K1[max_index[0], max_index[1], max_index[2]]
k2_vox = K2[max_index[0], max_index[1], max_index[2]]
Vp_vox = Vp[max_index[0], max_index[1], max_index[2]]

ct = osipi.extended_tofts(t, Ea, k1_vox, k1_vox / k2_vox, Vp_vox)
ct_real = E[max_index[0], max_index[1], max_index[2], :]
ct_extended = osipi.extended_tofts(t, Ea, k1, ve, vp)

plt.figure(figsize=(10, 6))
plt.plot(t, ct, label="ct_Mudified_Tofts")
plt.plot(t, ct_real, label="ct_Raw")
plt.plot(t, ct_extended, label="ct_Extended_Tofts")
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.title("ct_raw vs model")
plt.legend()
plt.show()

pvc_K1, pvc_k2, pvc_Vp = modifiedToftsMurase1Vox(Ea / (1 - Hct), Ev, dt, data_shape)
pvc = abs((1 - Hct) / pvc_Vp)  # sagittal sinus Vp should be 0.55, so calc correction factor if not

# Apply correction factor to fitted parameters
cor_K1 = K1 * pvc
cor_k2 = K2 * pvc
cor_Vp = Vp * pvc
# Apply Median Filter to parameters all with footprint (3,3)

mf_K1 = median_filter(cor_K1)
mf_k2 = median_filter(cor_k2)
mf_Vp = median_filter(cor_Vp)

mf_Vp[mf_Vp <= 0] = 0
mf_Vp[mf_Vp > 1] = 1.0
mf_K1[mf_K1 <= 0] = 0
mf_k2[mf_k2 <= 0] = 0

# evolve forwards model
aif_cor = np.max((Ea / (1 - Hct)) * pvc) / 6  # caluclate enhancement to concentration correction
Cp = (
    (Ea / (1 - Hct)) * pvc
) / aif_cor  # calculate Cp using signal enhancement aif and concentration conversion factor

c_tissue = ForwardsModTofts(mf_K1, mf_k2, mf_Vp, Cp, dt)

r1 = 3.9  # longitudinal relaxivity Gd-DTPA (Hz/mM) source: (Pintaske,2006)
r2st = 10  # transverse relaxivity Gd-DTPA (Hz/mM)
# roughly estimated using (Pintaske,2006) and (Siemonsen, 2008)

fa = np.deg2rad(float(dicom_ref.FlipAngle))  # flip angle (rads)

Te = 1e-3 * float(dicom_ref.EchoTime)  # Echo Time (s)
Tr = 1e-3 * float(dicom_ref.RepetitionTime)  # Repetition Time (s)
T1b = 1.48  # T1 for blood measured in sagittal sinus @ 1.5T (s) (Zhang et al., 2013)

R10_value = 1.18  # precontrast T1 relaxation rate (Hz) brain avg (radiopedia)
R20st_value = (
    17.24  # precontrast T1 relaxation rate (Hz) brain avg using T2* from (Siemonsen, 2008)
)
R10 = createR10_withref(
    S0ref, S0, Tr, fa, T1b, data_shape
)  # precontrast R1 map (normalised to sagittal sinus)

R1, R2st = calcR1_R2(R10, R20st_value, r1, r2st, c_tissue)  # returns R10 and R2st maps
dro_S, M = Conc2Sig_Linear(Tr, Te, fa, R1, R2st, S, 1, 0)

stdS = STDmap(signal, t0=5)  # caluclate Standard deviation for original data
dro_Snoise = addnoise(1, stdS, dro_S, Nt=data_shape[-1])

trans_K1 = mf_K1.copy()
trans_k2 = mf_k2.copy()
trans_Vp = mf_Vp.copy()

vmax_K1, vmax_k2, vmax_Vp = 1, 1, 0.2
vmin_K1, vmin_k2, vmin_Vp = 0.2, 0.2, 0.01
lb_K1, lb_k2, lb_Vp = 0.54, 0.52, 0.49
ub_K1, ub_k2, ub_Vp = 1.52, 1.5, 1.43
lim_K1, lim_k2, lim_Vp = vmax_K1 + 0.5, vmax_k2 + 0.1, vmax_Vp + 0.5
ub_lim = 1.01

trans_K1[trans_K1 <= vmin_K1] = trans_K1[trans_K1 <= vmin_K1] * lb_K1
trans_K1[trans_K1 >= lim_K1] = trans_K1[trans_K1 >= lim_K1] * ub_lim
trans_K1[(trans_K1 >= vmax_K1) & (trans_K1 < lim_K1)] = (
    trans_K1[(trans_K1 >= vmax_K1) & (trans_K1 < lim_K1)] * ub_K1
)
trans_K1[(trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)] = trans_K1[
    (trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)
] * (
    lb_K1
    + (
        ((trans_K1[(trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)] - vmin_K1) / (vmax_K1 - vmin_K1))
        * (ub_K1 - lb_K1)
    )
)

trans_k2[trans_k2 <= vmin_k2] = trans_k2[trans_k2 <= vmin_k2] * lb_k2
trans_k2[trans_k2 >= lim_k2] = trans_k2[trans_k2 >= lim_k2] * ub_lim
trans_k2[(trans_k2 >= vmax_k2) & (trans_k2 < lim_k2)] = (
    trans_k2[(trans_k2 >= vmax_k2) & (trans_k2 < lim_k2)] * ub_k2
)
trans_k2[(trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)] = trans_k2[
    (trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)
] * (
    lb_k2
    + (
        ((trans_k2[(trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)] - vmin_k2) / (vmax_k2 - vmin_k2))
        * (ub_k2 - lb_k2)
    )
)

trans_Vp[trans_Vp <= vmin_Vp] = trans_Vp[trans_Vp <= vmin_Vp] * lb_Vp
trans_Vp[(trans_Vp >= lim_Vp)] = trans_Vp[trans_Vp >= lim_Vp] * ub_lim
trans_Vp[(trans_Vp >= vmax_Vp) & (trans_Vp < lim_Vp)] = (
    trans_Vp[(trans_Vp >= vmax_Vp) & (trans_Vp < lim_Vp)] * ub_Vp
)
trans_Vp[(trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)] = trans_Vp[
    (trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)
] * (
    lb_Vp
    + (
        ((trans_Vp[(trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)] - vmin_Vp) / (vmax_Vp - vmin_Vp))
        * (ub_Vp - lb_Vp)
    )
)

trans_Vp[trans_Vp > 1] = 1

Ctiss_tr = ForwardsModTofts(trans_K1, trans_k2, trans_Vp, Cp, dt)

R1_tr, R2st_tr = calcR1_R2(R10, R20st_value, r1, r2st, Ctiss_tr)
dro_S_tr, M_tr = Conc2Sig_Linear(Tr, Te, fa, R1_tr, R2st_tr, signal, 1, M)

dro_Snoise_tr = addnoise(1, stdS, dro_S_tr, Nt=data_shape[-1])

animate_mri(signal, mode="time", slice_index=7, time_index=5)
animate_mri(dro_Snoise_tr, mode="time", slice_index=7, time_index=5)
animate_mri(dro_Snoise, mode="time", slice_index=7, time_index=5)
