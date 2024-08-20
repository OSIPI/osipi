import multiprocessing as mp

import numpy as np
from scipy.integrate import cumtrapz, trapz
from scipy.optimize import curve_fit

import osipi


def modifiedToftsMurase(Cp, Ctiss, dt, datashape):
    # Fit Modified Tofts (Linear from Murase, 2004)
    # Cp = Ea/0.45, Ctis=E/0.45
    # Matrix equation C=AB (same notation as Murase)
    # C: matrix of Ctis at distinct time steps
    # A: 3 Coumns, rows of tk:
    #   (1) Integral up to tk of Cp
    #   (2) - Integral up to tk of Ctiss
    #   (3) Cp at tk
    # B: Array length 3 of parameters:
    #   (1) K1 + k2 dot Vp
    #   (2) k2
    #   (3) Vp
    # Use np.linalg.solve for equations form Zx=y aimed to find x
    # np.linalg.solve(Z,y)=x  so need to use np.linalg.solve(A,C)
    # solve only works for square matrices so use .lstsq for a least squares solve
    #  Allocate parameter holding arrays

    K1 = np.zeros(Ctiss.shape[:-1])  # only spatial maps
    k2 = np.zeros(Ctiss.shape[:-1])  # only spatial maps
    Vp = np.zeros(Ctiss.shape[:-1])  # only spatial maps

    # Allocate matrices used from solver as defined above
    C = np.zeros(datashape[-1])
    A = np.zeros((datashape[-1], 3))

    # iterate over slices
    for k in range(0, datashape[2]):
        # iterate over rows
        for j in range(0, datashape[0]):
            # iterate over columns
            for i in range(0, datashape[1]):
                # Build matrices for Modified Tofts for voxel
                C = Ctiss[j, i, k, :]
                A[:, 0] = cumtrapz(Cp, dx=dt, initial=0)
                A[:, 1] = -cumtrapz(Ctiss[j, i, k, :], dx=dt, initial=0)
                A[:, 2] = Cp
                # Use least squares solver
                sing_B1, sing_k2, sing_Vp = np.linalg.lstsq(A, C, rcond=None)[0]
                sing_K1 = sing_B1 - (sing_k2 * sing_Vp)
                # Assign Ouputs into parameter maps
                K1[j, i, k] = sing_K1
                k2[j, i, k] = sing_k2
                Vp[j, i, k] = sing_Vp

    return K1, k2, Vp


def modifiedToftsMurase1Vox(Cp, Ctiss, dt, datashape):
    K1 = np.zeros(Ctiss.shape[:-1])  # only spatial maps
    k2 = np.zeros(Ctiss.shape[:-1])  # only spatial maps
    Vp = np.zeros(Ctiss.shape[:-1])  # only spatial maps

    # Allocate matrices used from solver as defined above
    C = np.zeros(datashape[-1])
    A = np.zeros((datashape[-1], 3))

    # Build matrices for Modified Tofts for voxel
    C = Ctiss
    A[:, 0] = cumtrapz(Cp, dx=dt, initial=0)
    A[:, 1] = -cumtrapz(Ctiss, dx=dt, initial=0)
    A[:, 2] = Cp
    # Use least squares solver
    B1, k2, Vp = np.linalg.lstsq(A, C, rcond=None)[0]
    K1 = B1 - (k2 * Vp)

    return K1, k2, Vp


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


def ForwardsModTofts(K1, k2, Vp, Cp, dt):
    # To be carried out as matmul C=BA
    # Where C is the output Ctiss and B the parameters
    # With A a matrix of cumulative integrals

    x, y, z = K1.shape
    t = Cp.shape[0]

    Ctiss = np.zeros((y, x, z, t))

    b1 = K1 + np.multiply(k2, Vp)  # define combined parameter
    B = np.zeros((x, y, z, 1, 3))
    A = np.zeros((x, y, z, 3, 1))

    B[:, :, :, 0, 0] = b1
    B[:, :, :, 0, 1] = -k2
    B[:, :, :, 0, 2] = Vp

    for tk in range(1, t):
        A[:, :, :, 0, 0] = trapz(Cp[0 : tk + 1], dx=dt)
        A[:, :, :, 1, 0] = trapz(Ctiss[:, :, :, 0 : tk + 1], dx=dt)
        A[:, :, :, 2, 0] = Cp[tk]

        Ctiss[:, :, :, tk] = np.matmul(B, A).squeeze()
    return Ctiss


def ForwardsModTofts_1vox(K1, k2, Vp, Cp, dt):
    # To be carried out as matmul C=BA
    # Where C is the output Ctiss and B the parameters
    # With A a matrix of cumulative integrals

    t = Cp.shape[0]

    Ctiss = np.zeros(t)

    b1 = K1 + k2 * Vp  # define combined parameter
    B = np.zeros((1, 3))
    A = np.zeros((3, 1))

    B[0][0] = b1
    B[0][1] = -k2
    B[0][2] = Vp

    for tk in range(1, t):
        A[0][0] = trapz(Cp[0 : tk + 1], dx=dt)
        A[1][0] = trapz(Ctiss[0 : tk + 1], dx=dt)
        A[2][0] = Cp[tk]

        Ctiss[tk] = np.matmul(B, A).squeeze()
    return Ctiss
