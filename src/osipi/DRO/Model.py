import numpy as np
from scipy.integrate import cumtrapz, trapz


def tofts(cp, c_tiss, dt, datashape):
    """
    Tofts model for DCE-MRI DRO

    ref : https://github.com/JCardenasRdz/Gage-repeatability-DCE-MRI?tab=readme-ov-file

    """
    ktrans = np.zeros(c_tiss.shape[:-1])
    kep = np.zeros(c_tiss.shape[:-1])

    for k in range(0, datashape[2]):
        for j in range(0, datashape[0]):
            for i in range(0, datashape[1]):
                c = c_tiss[j, i, k, :]
                cp_integrated = cumtrapz(cp, dx=dt, initial=0)
                c_tiss_integrated = -cumtrapz(c_tiss[i, j, k, :], dx=dt, initial=0)
                A = np.column_stack((cp_integrated, c_tiss_integrated))
                ktrans_voxel, kep_voxel = np.linalg.lstsq(A, c, rcond=None)[0]
                ktrans[j, i, k] = ktrans_voxel
                kep[j, i, k] = kep_voxel

    return ktrans, kep


def exntended_tofts(cp, c_tiss, dt, datashape):
    """
    Extended Tofts model for DCE-MRI DRO

    """
    ktrans = np.zeros(c_tiss.shape[:-1])
    kep = np.zeros(c_tiss.shape[:-1])
    vp = np.zeros(c_tiss.shape[:-1])

    for k in range(0, datashape[2]):
        for j in range(0, datashape[0]):
            for i in range(0, datashape[1]):
                c = c_tiss[j, i, k, :]
                cp_integrated = cumtrapz(cp, dx=dt, initial=0)
                c_tiss_integrated = -cumtrapz(c_tiss[i, j, k, :], dx=dt, initial=0)
                A = np.column_stack((cp_integrated, c_tiss_integrated, cp))
                ktrans_voxel, kep_voxel, vp_voxel = np.linalg.lstsq(A, c, rcond=None)[0]
                ktrans[j, i, k] = ktrans_voxel
                kep[j, i, k] = kep_voxel
                vp[j, i, k] = vp_voxel

    return ktrans, kep, vp


def forward_tofts(ktrans, kep, cp, vp, dt):
    """
    Forward Tofts model for DCE-MRI DRO

    Parameters:
    ktrans (numpy.ndarray): The transfer constant Ktrans.
    kep (numpy.ndarray): The rate constant kep.
    cp (numpy.ndarray): The plasma concentration C_p(t).
    vp (numpy.ndarray): The plasma volume fraction v_p.
    dt (float): The time step between measurements.

    Returns:
    numpy.ndarray: The tissue concentration C_tiss(t).
    """
    time_points = cp.shape[-1]
    c_tiss = np.zeros(ktrans.shape)
    for t in range(time_points):
        if t == 0:
            c_tiss[..., t] = vp * cp[..., t]
        else:
            exp = np.exp(-kep * np.arange(t + 1)[::-1] * dt)
            integral = trapz(cp[..., : t + 1] * exp, dx=dt, axis=-1)
            c_tiss[..., t] = vp * cp[..., t] + ktrans * integral

    return c_tiss
