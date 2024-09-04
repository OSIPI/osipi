import multiprocessing as mp

import numpy as np
from scipy.optimize import curve_fit

import osipi


def fit_single_voxel_extended_tofts(ct, ca, time):
    def fit_func_ET(t, kt, ve, vp):
        return osipi.extended_tofts(t, ca, kt, ve, vp)

    ini = [0, 0, 0]
    popt, pcov = curve_fit(fit_func_ET, time, ct, p0=ini)
    return popt


def fit_single_voxel_tofts(ct, ca, time):
    def fit_func_T(t, kt, ve):
        return osipi.tofts(t, ca, kt, ve)

    ini = [0, 0]
    popt, pcov = curve_fit(fit_func_T, time, ct, p0=ini)
    return popt


def process_voxel(j, i, k, c_tiss, ca, t, type="ET"):
    ct = c_tiss[j, i, k, :]
    if type == "ET":
        popt = fit_single_voxel_extended_tofts(ct, ca, t)
    elif type == "T":
        popt = fit_single_voxel_tofts(ct, ca, t)
    return j, i, k, popt


def extended_tofts_model(ca, c_tiss, t):
    ktrans = np.zeros(c_tiss.shape[:-1])
    ve = np.zeros(c_tiss.shape[:-1])
    vp = np.zeros(c_tiss.shape[:-1])

    tasks = [
        (j, i, k, c_tiss, ca, t)
        for k in range(c_tiss.shape[2])
        for j in range(c_tiss.shape[0])
        for i in range(c_tiss.shape[1])
    ]

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_voxel, tasks)

    for j, i, k, popt in results:
        ktrans[j, i, k], ve[j, i, k], vp[j, i, k] = popt

    return ktrans, ve, vp


def extended_tofts_model_1vox(ca, c_tiss, t):
    """
    Extended Tofts model for DCE-MRI DRO
    ca -- arterial input function
    c_tiss -- 1D array of tissue concentration data (time)
    dt -- time interval between samples
    """

    ct = c_tiss[:]
    popt = fit_single_voxel_extended_tofts(ct, ca, t)

    return popt


def forward_extended_tofts(K1, Ve, Vp, Ca, time):
    x, y, z = K1.shape
    t = Ca.shape[0]
    c_tiss = np.zeros((y, x, z, t))

    for k in range(0, K1.shape[2]):
        for j in range(0, K1.shape[0]):
            for i in range(0, K1.shape[1]):
                c_tiss[i, j, k, :] = osipi.extended_tofts(
                    time, Ca, K1[i, j, k], Ve[i, j, k], Vp[i, j, k]
                )

    return c_tiss


def tofts_model(ca, c_tiss, t):
    ktrans = np.zeros(c_tiss.shape[:-1])
    ve = np.zeros(c_tiss.shape[:-1])

    tasks = [
        (j, i, k, c_tiss, ca, t, "T")
        for k in range(c_tiss.shape[2])
        for j in range(c_tiss.shape[0])
        for i in range(c_tiss.shape[1])
    ]

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_voxel, tasks)

    for j, i, k, popt in results:
        ktrans[j, i, k], ve[j, i, k] = popt

    return ktrans, ve
