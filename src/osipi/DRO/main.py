import numpy as np
import pydicom

import osipi.DRO as dro

if __name__ == "__main__":
    uidprefix = "1.3.6.1.4.1.9328.50.16."
    study_instance_uid = pydicom.uid.generate_uid(prefix=uidprefix)
    dro_IDnum = "9215224289"

    signal, slices, dicom_ref = dro.read_dicom_slices_as_4d_signal(
        "data/subject2/12.000000-perfusion-17557"
    )
    # shape of the mri data
    data_shape = signal.shape

    # extract the signal enhancement
    # E is the signal enhancement, S0 is the baseline signal, signal is the original signal
    E, S0, signal = dro.signal_enhancement_extract(signal, data_shape, 5)

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

    Ea = dro.ic_from_roi(E, aifmask, roivoxa, aifmask.ndim - 1)
    Ev = dro.ic_from_roi(E, sagmask, roivoxv, sagmask.ndim - 1)
    S0ref = dro.ic_from_roi(S0[:, :, z], sagmask[:, :, z, 0], roivoxv, sagmask.ndim - 2)

    # choose a voxel with maximum enhancement to display the fitting process
    max_index = np.unravel_index(np.argmax(E * aifmask, axis=None), E.shape)

    # hematocrit value for partial volume correction
    hct = 0.45

    # fitting using extended tofts model for first 8 slices
    # choose only first 8 slices due to memory constrains
    kt, ve, vp = dro.extended_tofts_model(Ea, E[:, :, :8, :], t)

    # A partial volume correction was applied using the sagittal sinus signal.
    pvc_K1, pvc_Ve, pvc_Vp = dro.extended_tofts_model_1vox(Ea, Ev, t)
    pvc = abs(
        (1 - hct) / pvc_Vp
    )  # sagittal sinus Vp should be 0.55, so calc correction factor if not

    # Apply correction factor to fitted parameters
    cor_Kt = kt * pvc
    cor_Ve = ve * pvc
    cor_Vp = vp * pvc

    # Apply Median Filter to parameters all with footprint (3,3)
    mf_Kt = dro.median_filter(cor_Kt)
    mf_Ve = dro.median_filter(cor_Ve)
    mf_Vp = dro.median_filter(cor_Vp)

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
    c_tissue = dro.forward_extended_tofts(mf_Kt, mf_Ve, mf_Vp, (Ea / aif_cor), t)

    # Choosing a specific voxel to plot Concentration curves and the fitting process
    kt_vox1 = mf_Kt[96, 118, 5]
    ve_vox1 = mf_Ve[96, 118, 5]
    vp_vox1 = mf_Vp[96, 118, 5]

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
    R10 = dro.createR10_withref(
        S0ref, S0[:, :, :8], Tr, fa, T1b, data_shape
    )  # precontrast R1 map (normalised to sagittal sinus)

    R1, R2st = dro.calcR1_R2(R10, R20st_value, r1, r2st, c_tissue)  # returns R10 and R2st maps

    # calculate the signal using the concentration and relaxation rates
    # spoiled gradient echo sequence
    dro_s, M = dro.Conc2Sig_Linear(Tr, Te, fa, R1, R2st, signal[:, :, :8, :], 1, 0)

    stdS = dro.STDmap(signal[:, :, :8, :], t0=5)  # caluclate Standard deviation for original data
    # add noise to the signal
    dro_s_noise = dro.addnoise(1, stdS, dro_s, Nt=data_shape[-1])

    trans_Kt = mf_Kt.copy()
    trans_Ve = mf_Ve.copy()
    trans_Vp = mf_Vp.copy()

    vmax_Kt, vmax_ke, vmax_Vp = 1, 1, 0.2
    vmin_Kt, vmin_ke, vmin_Vp = 0.2, 0.2, 0.01
    lb_Kt, lb_ke, lb_Vp = 0.54, 0.52, 0.49
    ub_Kt, ub_ke, ub_Vp = 1.52, 1.5, 1.43
    lim_Kt, lim_ke, lim_Vp = vmax_Kt + 0.5, vmax_ke + 0.1, vmax_Vp + 0.5
    ub_lim = 1.01

    trans_Kt[trans_Kt <= vmin_Kt] = trans_Kt[trans_Kt <= vmin_Kt] * lb_Kt
    trans_Kt[trans_Kt >= lim_Kt] = trans_Kt[trans_Kt >= lim_Kt] * ub_lim
    trans_Kt[(trans_Kt >= vmax_Kt) & (trans_Kt < lim_Kt)] = (
        trans_Kt[(trans_Kt >= vmax_Kt) & (trans_Kt < lim_Kt)] * ub_Kt
    )
    trans_Kt[(trans_Kt > vmin_Kt) & (trans_Kt < vmax_Kt)] = trans_Kt[
        (trans_Kt > vmin_Kt) & (trans_Kt < vmax_Kt)
    ] * (
        lb_Kt
        + (
            (
                (trans_Kt[(trans_Kt > vmin_Kt) & (trans_Kt < vmax_Kt)] - vmin_Kt)
                / (vmax_Kt - vmin_Kt)
            )
            * (ub_Kt - lb_Kt)
        )
    )

    trans_Vp[trans_Vp > 1] = 1

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
            (
                (trans_Vp[(trans_Vp > vmin_Vp) & (trans_Vp < vmax_Vp)] - vmin_Vp)
                / (vmax_Vp - vmin_Vp)
            )
            * (ub_Vp - lb_Vp)
        )
    )

    c_tissue_tr = dro.forward_extended_tofts(trans_Kt, trans_Ve, trans_Vp, (Ea / aif_cor), t)

    R1_tr, R2st_tr = dro.calcR1_R2(R10, R20st_value, r1, r2st, c_tissue_tr)
    dro_s_tr, M_tr = dro.Conc2Sig_Linear(Tr, Te, fa, R1_tr, R2st_tr, signal[:, :, :8, :], 1, M)

    dro_s_noise_tr = dro.addnoise(1, stdS, dro_s_tr, Nt=data_shape[-1])

    dro.animate_mri(signal, mode="time", slice_index=7, time_index=5)
    dro.animate_mri(dro_s_noise_tr, mode="time", slice_index=7, time_index=5)
    dro.animate_mri(dro_s_noise, mode="time", slice_index=7, time_index=5)

    save = True

    if save:
        dro.save_dicoms("output", slices, dro_s_noise, dro_IDnum, study_instance_uid)
