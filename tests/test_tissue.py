import math

import numpy as np
import osipi
import pytest


@pytest.fixture
def time_array():
    return np.arange(0, 6 * 60, 1)


@pytest.fixture
def aif(time_array):
    return osipi.aif_parker(time_array)


@pytest.fixture
def base_params():
    return {"Ktrans": 0.6, "ve": 0.2}


def test_tissue_tofts(time_array, aif, base_params):
    """1.  Basic operation of the function - test that the peak tissue concentration is less than the peak
    AIF

    """
    ct = osipi.tofts(time_array, aif, discretization_method="exp", **base_params)
    assert np.round(np.max(ct)) < np.round(np.max(aif))

    # 2. Basic operation of the function - test with non-uniform spacing of
    # time array
    t = np.geomspace(1, 6 * 60 + 1, num=360) - 1
    ca = osipi.aif_parker(t)
    ct = osipi.tofts(t, ca, Ktrans=0.6, ve=0.2)
    assert np.round(np.max(ct)) < np.round(np.max(ca))

    # 3. The offset option - test that the tissue concentration is shifted
    # from the AIF by the specified offset time
    ct = osipi.tofts(time_array, aif, Ta=60.0, **base_params)
    assert (np.min(np.where(ct > 0.0)) - np.min(np.where(aif > 0.0)) - 1) * 1 == 60.0

    # 4. Test that the discretization options give almost the same result -
    # time step must be very small
    t = np.arange(0, 6 * 60, 0.01)
    ca = osipi.aif_parker(t)
    ct_conv = osipi.tofts(t, ca, **base_params)
    ct_exp = osipi.tofts(t, ca, discretization_method="exp", **base_params)
    assert np.allclose(ct_conv, ct_exp, rtol=1e-4, atol=1e-3)

    # 5. Test that the ratio of the area under the ct and ca curves is
    # approximately the extracellular volume

    ct_conv = osipi.tofts(time_array, aif, **base_params)
    ct_exp = osipi.tofts(time_array, aif, discretization_method="exp", **base_params)
    assert math.isclose(
        np.trapz(ct_conv, time_array) / np.trapz(aif, time_array), 0.2, abs_tol=1e-1
    )
    assert math.isclose(np.trapz(ct_exp, time_array) / np.trapz(aif, time_array), 0.2, abs_tol=1e-1)

    # 6. Test specific use cases
    ct_conv = osipi.tofts(time_array, aif, Ktrans=0, ve=0.2)
    assert np.count_nonzero(ct_conv) == 0

    ct_exp = osipi.tofts(time_array, aif, Ktrans=0, ve=0.2, discretization_method="exp")
    assert np.count_nonzero(ct_exp) == 0

    ct_conv = osipi.tofts(time_array, aif, Ktrans=0.6, ve=0)
    assert np.count_nonzero(ct_conv) == 0

    ct_exp = osipi.tofts(time_array, aif, Ktrans=0.6, ve=0, discretization_method="exp")
    assert np.count_nonzero(ct_exp) == 0


def test_tissue_extended_tofts(time_array, aif):
    # 1. Basic operation of the function - test that the peak tissue
    # concentration is less than the peak AIF
    t = np.linspace(0, 6 * 60, 360)
    ca = osipi.aif_parker(t)
    ct = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3)
    assert np.round(np.max(ct)) < np.round(np.max(ca))

    # 2. Basic operation of the function - test with non-uniform spacing of
    # time array
    t = np.geomspace(1, 6 * 60 + 1, num=360) - 1
    ca = osipi.aif_parker(t)
    ct = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3)
    assert np.round(np.max(ct)) < np.round(np.max(ca))

    # 3. The offset option - test that the tissue concentration is shifted
    # from the AIF by the specified offset time
    ct = osipi.extended_tofts(time_array, aif, Ktrans=0.6, ve=0.2, vp=0.3, Ta=60.0)
    assert (np.min(np.where(ct > 0.0)) - np.min(np.where(aif > 0.0)) - 1) * 1 == 60.0

    # 4. Test that the discretization options give almost the same result -
    # time step must be very small
    t = np.arange(0, 6 * 60, 0.01)
    ca = osipi.aif_parker(t)
    ct_conv = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3)
    ct_exp = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3, discretization_method="exp")
    assert np.allclose(ct_conv, ct_exp, rtol=1e-4, atol=1e-3)

    # 5. Test that the ratio of the area under the ct and ca curves is
    # approximately the extracellular volume plus the plasma volume
    ct_conv = osipi.extended_tofts(time_array, aif, Ktrans=0.6, ve=0.2, vp=0.3)
    ct_exp = osipi.extended_tofts(
        time_array, aif, Ktrans=0.6, ve=0.2, vp=0.3, discretization_method="exp"
    )
    assert math.isclose(
        np.trapz(ct_conv, time_array) / np.trapz(aif, time_array),
        0.2 + 0.3,
        abs_tol=1e-1,
    )
    assert math.isclose(
        np.trapz(ct_exp, time_array) / np.trapz(aif, time_array), 0.2 + 0.3, abs_tol=1e-1
    )

    # 6. Test specific use cases

    ct_conv = osipi.extended_tofts(time_array, aif, Ktrans=0, ve=0.2, vp=0.3)
    assert np.allclose(ct_conv, aif * 0.3, rtol=1e-4, atol=1e-3)

    ct_exp = osipi.extended_tofts(
        time_array, aif, Ktrans=0, ve=0.2, vp=0.3, discretization_method="exp"
    )
    assert np.allclose(ct_conv, aif * 0.3, rtol=1e-4, atol=1e-3)

    ct_conv = osipi.extended_tofts(time_array, aif, Ktrans=0.6, ve=0, vp=0.3)
    assert np.allclose(ct_conv, aif * 0.3, rtol=1e-4, atol=1e-3)

    ct_exp = osipi.extended_tofts(
        time_array, aif, Ktrans=0.6, ve=0, vp=0.3, discretization_method="exp"
    )
    assert np.allclose(ct_conv, aif * 0.3, rtol=1e-4, atol=1e-3)


@pytest.mark.parametrize(
    "time_points",
    [
        (np.linspace(0, 6 * 60, 360), "uniform"),
        (np.geomspace(1, 6 * 60 + 1, num=360) - 1, "non-uniform"),
    ],
)
def test_2cxm_basic_operation(time_points):
    """Test that the peak tissue concentration is less than the peak AIF for different time arrays"""
    t, _ = time_points
    ca = osipi.aif_parker(t)
    ct = osipi.two_compartment_exchange_model(t, ca, Fp=10, PS=5, ve=0.2, vp=0.3)
    assert np.round(np.max(ct)) < np.round(np.max(ca))


def test_2cxm_time_offset(time_array, aif):
    """Test that the tissue concentration is shifted from the AIF by the specified offset time"""
    ct = osipi.two_compartment_exchange_model(time_array, aif, Fp=10, PS=5, ve=0.2, vp=0.3, Ta=60.0)
    assert (np.min(np.where(ct > 0.0)) - np.min(np.where(aif > 0.0)) - 1) * 1 == 60.0


def test_2cxm_zero_vp_matches_tofts(time_array, aif):
    """Test that 2CXM with vp=0 behaves like the Tofts model"""
    ct = osipi.two_compartment_exchange_model(time_array, aif, Fp=10, PS=5, ve=0.2, vp=0)
    ct_tofts = osipi.tofts(time_array, aif, Ktrans=3.93, ve=0.2)
    assert np.allclose(ct, ct_tofts, rtol=1e-4, atol=1e-3)


if __name__ == "__main__":
    pytest.main([__file__])
