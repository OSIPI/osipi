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
    extended_tofts_model,
    extended_tofts_model_1vox,
    forward_extended_tofts,
)

if __name__ == "__main__":
    signal, slices, dicom_ref = read_dicom_slices_as_4d_signal(
        "data/subject2/12.000000-perfusion-17557"
    )
    # shape of the mri data
    data_shape = signal.shape

    # extract the signal enhancement
    # E is the signal enhancement, S0 is the baseline signal, signal is the original signal
    E, S0, signal = SignalEnhancementExtract(signal, data_shape, 5)

    dt = 4.8 / 60  # mins from the RIDER website DCE description
    t = np.linspace(0, dt * signal.shape[-1], signal.shape[-1])  # time series points

    # load the ROI masks
    # Will be added to create ROI masks from the GUI not just saved ones

    aif_dir = "ROI_saved/"

    aifmask = np.load("{}aifmask.npy".format(aif_dir))
    sagmask = np.load("{}sagmask.npy".format(aif_dir))
    roivoxa = np.load("{}aifmaskvox.npy".format(aif_dir))
    roivoxv = np.load("{}sagmaskvox.npy".format(aif_dir))

    z = 5

    Ea = ICfromROI(E, aifmask, roivoxa, aifmask.ndim - 1)
    Ev = ICfromROI(E, sagmask, roivoxv, sagmask.ndim - 1)
    S0ref = ICfromROI(S0[:, :, z], sagmask[:, :, z, 0], roivoxv, sagmask.ndim - 2)

    # choose a voxel with maximum enhancement to display the fitting process
    max_index = np.unravel_index(np.argmax(E * aifmask, axis=None), E.shape)
    print(max_index)

    # hematocrit value for partial volume correction
    hct = 0.45

    # fitting using extended tofts model for first 8 slices
    # choose only first 8 slices due to memory constrains
    kt, ve, vp = extended_tofts_model(Ea, E[:, :, :8, :], t)

    # A partial volume correction was applied using the sagittal sinus signal.
    pvc_K1, pvc_Ve, pvc_Vp = extended_tofts_model_1vox(Ea, Ev, t)
    pvc = abs(
        (1 - hct) / pvc_Vp
    )  # sagittal sinus Vp should be 0.55, so calc correction factor if not

    # Apply correction factor to fitted parameters
    cor_Kt = kt * pvc
    cor_Ve = ve * pvc
    cor_Vp = vp * pvc

    # Apply Median Filter to parameters all with footprint (3,3)
    mf_Kt = median_filter(cor_Kt)
    mf_Ve = median_filter(cor_Ve)
    mf_Vp = median_filter(cor_Vp)

    # Apply thresholds to remove negative values
    # limit volume fraction to max value of 1
    mf_Vp[mf_Vp <= 0] = 0
    mf_Vp[mf_Vp > 1] = 1.0
    mf_Ve[mf_Ve > 1] = 1.0
    mf_Kt[mf_Kt <= 0] = 0
    mf_Ve[mf_Ve <= 0] = 0

    # the aif signal is corrected with hematocrit, scaled to 6mM as a realistic value

    aif_cor = np.max((Ea / (1 - hct)) * pvc) / 6

    # caluclate enhancement to concentration correction
    # Cp = (
    #     (Ea / (1 - hct)) * pvc
    # ) / aif_cor  # calculate Cp using signal enhancement aif and concentration conversion factor

    # calculate the concentration in the tissue using the fitted parameters
    c_tissue = forward_extended_tofts(mf_Kt, mf_Ve, mf_Vp, (Ea / aif_cor), t)

    # Choosing a specific voxel to plot Concentration curves and the fitting process
    kt_vox1 = mf_Kt[96, 118, 5]
    ve_vox1 = mf_Ve[96, 118, 5]
    vp_vox1 = mf_Vp[96, 118, 5]

    # calculate the fitted concentration to compare with the real one
    c_tissue_tofts = osipi.extended_tofts(t, Ea, kt_vox1, ve_vox1, vp_vox1)

    plt.figure(figsize=(10, 6))
    plt.plot(t, c_tissue_tofts, label="ct_Tofts")
    plt.plot(t, E[96, 118, 5, :], label="Ct_raw")
    plt.xlabel("Time")
    plt.ylabel("Concentration")
    plt.title("ct_raw vs model")
    plt.legend()
    plt.show()

    # calculate the relaxation rates R1 and R2* for the tissue

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
        S0ref, S0[:, :, :8], Tr, fa, T1b, data_shape
    )  # precontrast R1 map (normalised to sagittal sinus)

    R1, R2st = calcR1_R2(R10, R20st_value, r1, r2st, c_tissue)  # returns R10 and R2st maps

    # calculate the signal using the concentration and relaxation rates
    # spoiled gradient echo sequence
    dro_S, M = Conc2Sig_Linear(Tr, Te, fa, R1, R2st, signal[:, :, :8, :], 1, 0)

    stdS = STDmap(signal[:, :, :8, :], t0=5)  # caluclate Standard deviation for original data
    # add noise to the signal
    dro_Snoise = addnoise(1, stdS, dro_S, Nt=data_shape[-1])
    animate_mri(dro_Snoise, mode="time", slice_index=7, time_index=5)

    #
    # trans_K1 = mf_K1.copy()
    # trans_k2 = mf_k2.copy()
    # trans_Vp = mf_Vp.copy()
    #
    # vmax_K1, vmax_k2, vmax_Vp = 1, 1, 0.2
    # vmin_K1, vmin_k2, vmin_Vp = 0.2, 0.2, 0.01
    # lb_K1, lb_k2, lb_Vp = 0.54, 0.52, 0.49
    # ub_K1, ub_k2, ub_Vp = 1.52, 1.5, 1.43
    # lim_K1, lim_k2, lim_Vp = vmax_K1 + 0.5, vmax_k2 + 0.1, vmax_Vp + 0.5
    # ub_lim = 1.01
    #
    # trans_K1[trans_K1 <= vmin_K1] = trans_K1[trans_K1 <= vmin_K1] * lb_K1
    # trans_K1[trans_K1 >= lim_K1] = trans_K1[trans_K1 >= lim_K1] * ub_lim
    # trans_K1[(trans_K1 >= vmax_K1) & (trans_K1 < lim_K1)] = (
    #     trans_K1[(trans_K1 >= vmax_K1) & (trans_K1 < lim_K1)] * ub_K1
    # )
    # trans_K1[(trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)] = trans_K1[
    #     (trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)
    # ] * (
    #     lb_K1
    #     + (
    #         (
    #             (trans_K1[(trans_K1 > vmin_K1) & (trans_K1 < vmax_K1)] - vmin_K1)
    #             / (vmax_K1 - vmin_K1)
    #         )
    #         * (ub_K1 - lb_K1)
    #     )
    # )
    #
    # trans_k2[trans_k2 <= vmin_k2] = trans_k2[trans_k2 <= vmin_k2] * lb_k2
    # trans_k2[trans_k2 >= lim_k2] = trans_k2[trans_k2 >= lim_k2] * ub_lim
    # trans_k2[(trans_k2 >= vmax_k2) & (trans_k2 < lim_k2)] = (
    #     trans_k2[(trans_k2 >= vmax_k2) & (trans_k2 < lim_k2)] * ub_k2
    # )
    # trans_k2[(trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)] = trans_k2[
    #     (trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)
    # ] * (
    #     lb_k2
    #     + (
    #         (
    #             (trans_k2[(trans_k2 > vmin_k2) & (trans_k2 < vmax_k2)] - vmin_k2)
    #             / (vmax_k2 - vmin_k2)
    #         )
    #         * (ub_k2 - lb_k2)
    #     )
    # )
    #
    # trans_Vp[trans_Vp <= vmin_Vp] = trans_Vp[trans_Vp <= vmin_Vp] * lb_Vp
    # trans_Vp[(trans_Vp >= lim_Vp)] = trans_Vp[trans_Vp >= lim_Vp] * ub_lim
    # trans_Vp[(trans_Vp >= vmax_Vp) & (trans_Vp < lim_Vp)] = (
    #     trans_Vp[(trans_Vp >= vmax_Vp) & (trans_Vp < lim_Vp)] * ub_Vp
    # )
    # trans_Vp[(trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)] = trans_Vp[
    #     (trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)
    # ] * (
    #     lb_Vp
    #     + (
    #         (
    #             (trans_Vp[(trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)] - vmin_Vp)
    #             / (vmax_Vp - vmin_Vp)
    #         )
    #         * (ub_Vp - lb_Vp)
    #     )
    # )
    #
    # trans_Vp[trans_Vp > 1] = 1
    #
    # Ctiss_tr = forward_extended_tofts(trans_K1, trans_k2, trans_Vp, Ea, t)
    #
    # R1_tr, R2st_tr = calcR1_R2(R10, R20st_value, r1, r2st, Ctiss_tr)
    # dro_S_tr, M_tr = Conc2Sig_Linear(Tr, Te, fa, R1_tr, R2st_tr, signal[:, :, :8, :], 1, M)
    #
    # dro_Snoise_tr = addnoise(1, stdS, dro_S_tr, Nt=data_shape[-1])
    #
    # animate_mri(signal, mode="time", slice_index=7, time_index=5)
    # animate_mri(dro_Snoise_tr, mode="time", slice_index=7, time_index=5)
    # animate_mri(dro_Snoise, mode="time", slice_index=7, time_index=5)
