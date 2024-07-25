import numpy as np
from scipy.integrate import cumtrapz, trapz


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
