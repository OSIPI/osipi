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


# Tests for the Tofts model


@pytest.mark.parametrize(
    "t",
    [np.arange(0, 6 * 60, 1), np.geomspace(1, 6 * 60 + 1, num=360) - 1],
    ids=["uniform", "non-uniform"],
)
def test_tofts_peak_concentration(t, aif):
    """Test peak tissue concentration is less than peak AIF"""
    ct = osipi.tofts(t, aif, Ktrans=0.6, ve=0.2)
    assert np.round(np.max(ct)) < np.round(np.max(aif))


def test_tofts_time_offset(time_array, aif):
    """Test tissue concentration is shifted by specified offset time"""
    ct = osipi.tofts(time_array, aif, Ktrans=0.6, ve=0.2, Ta=60.0)
    offset_diff = (np.min(np.where(ct > 0.0)) - np.min(np.where(aif > 0.0)) - 1) * 1
    assert offset_diff == 60.0


def test_tofts_discretization_agreement():
    """Test different discretization methods give similar results with small time steps"""
    t = np.arange(0, 6 * 60, 0.01)
    ca = osipi.aif_parker(t)
    ct_conv = osipi.tofts(t, ca, Ktrans=0.6, ve=0.2)
    ct_exp = osipi.tofts(t, ca, Ktrans=0.6, ve=0.2, discretization_method="exp")
    assert np.allclose(ct_conv, ct_exp, rtol=1e-4, atol=1e-3)


@pytest.mark.parametrize("method", [None, "exp"], ids=["conv", "exp"])
def test_tofts_volume_ratio(time_array, aif, method):
    """Test ratio of AUC matches extracellular volume"""
    ct = osipi.tofts(time_array, aif, Ktrans=0.6, ve=0.2, discretization_method=method)
    ratio = np.trapz(ct, time_array) / np.trapz(aif, time_array)
    assert math.isclose(ratio, 0.2, abs_tol=1e-1)


@pytest.mark.parametrize("Ktrans, ve", [(0, 0.2), (0.6, 0)], ids=["Ktrans=0", "ve=0"])
@pytest.mark.parametrize("method", [None, "exp"], ids=["conv", "exp"])
def test_tofts_specific_cases(time_array, aif, Ktrans, ve, method):
    """Test edge cases with parameter combinations"""
    ct = osipi.tofts(time_array, aif, Ktrans=Ktrans, ve=ve, discretization_method=method)
    assert np.count_nonzero(ct) == 0


@pytest.mark.parametrize(
    "param, value, match",
    [
        ("Ktrans", -0.1, "non-negative"),
        ("Ktrans", "invalid", "numeric scalar"),
        ("ve", -0.2, "in range \[0, 1\]"),
        ("ve", [0.2], "numeric scalar"),
        ("Ta", -5.0, "non-negative"),
    ],
    ids=["Ktrans_negative", "Ktrans_type", "ve_negative", "ve_type", "Ta_negative"],
)
def test_tofts_invalid_parameters(time_array, aif, param, value, match):
    """Test invalid parameter values/type for all model parameters"""
    with pytest.raises((ValueError, TypeError), match=match):
        # Construct kwargs with one invalid parameter at a time
        kwargs = {"Ktrans": 0.6, "ve": 0.2, "Ta": 30.0}
        kwargs[param] = value
        osipi.tofts(time_array, aif, **kwargs)


# Tests for the Extended Tofts model


@pytest.mark.parametrize(
    "t",
    [np.linspace(0, 6 * 60, 360), np.geomspace(1, 6 * 60 + 1, num=360) - 1],
    ids=["uniform", "non-uniform"],
)
def test_extended_tofts_peak_concentration(t):
    """Test peak tissue concentration is less than peak AIF for different time arrays"""
    ca = osipi.aif_parker(t)
    ct = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3)
    assert np.round(np.max(ct)) < np.round(np.max(ca))


def test_extended_tofts_time_offset(time_array, aif):
    """Test tissue concentration is shifted by specified offset time"""
    ct = osipi.extended_tofts(time_array, aif, Ktrans=0.6, ve=0.2, vp=0.3, Ta=60.0)
    offset_diff = (np.min(np.where(ct > 0.0)) - np.min(np.where(aif > 0.0)) - 1) * 1
    assert offset_diff == 60.0


def test_extended_tofts_discretization_agreement():
    """Test different discretization methods give similar results with small time steps"""
    t = np.arange(0, 6 * 60, 0.01)
    ca = osipi.aif_parker(t)
    ct_conv = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3)
    ct_exp = osipi.extended_tofts(t, ca, Ktrans=0.6, ve=0.2, vp=0.3, discretization_method="exp")
    assert np.allclose(ct_conv, ct_exp, rtol=1e-4, atol=1e-3)


@pytest.mark.parametrize("method", [None, "exp"], ids=["conv", "exp"])
def test_extended_tofts_volume_ratio(time_array, aif, method):
    """Test ratio of AUC matches ve + vp for different discretization methods"""
    ct = osipi.extended_tofts(
        time_array, aif, Ktrans=0.6, ve=0.2, vp=0.3, discretization_method=method
    )
    ratio = np.trapz(ct, time_array) / np.trapz(aif, time_array)
    assert math.isclose(ratio, 0.2 + 0.3, abs_tol=1e-1)


@pytest.mark.parametrize("Ktrans, ve", [(0, 0.2), (0.6, 0)], ids=["Ktrans=0", "ve=0"])
@pytest.mark.parametrize("method", [None, "exp"], ids=["conv", "exp"])
def test_extended_tofts_specific_cases(time_array, aif, Ktrans, ve, method):
    """Test edge cases with parameter combinations"""
    ct = osipi.extended_tofts(
        time_array, aif, Ktrans=Ktrans, ve=ve, vp=0.3, discretization_method=method
    )
    expected = aif * 0.3
    assert np.allclose(ct, expected, rtol=1e-4, atol=1e-3)


@pytest.mark.parametrize(
    "param, value, match",
    [
        ("Ktrans", -0.1, "non-negative"),
        ("Ktrans", "invalid", "numeric scalar"),
        ("ve", -0.2, "in range \[0, 1\]"),
        ("ve", [0.2], "numeric scalar"),
        ("vp", -0.2, "in range \[0, 1\]"),
        ("vp", [0.2], "numeric scalar"),
        ("vp", 1.1, "in range \[0, 1\]"),
        ("vp", [0.2], "numeric scalar"),
        ("Ta", -5.0, "non-negative"),
    ],
    ids=[
        "Ktrans_negative",
        "Ktrans_type",
        "ve_negative",
        "ve_type",
        "vp_negative",
        "vp_type",
        "vp_range",
        "vp_type",
        "Ta_negative",
    ],
)
def test_extended_tofts_invalid_parameters(time_array, aif, param, value, match):
    """Test invalid parameter values/type for all model parameters"""
    with pytest.raises((ValueError, TypeError), match=match):
        # Construct kwargs with one invalid parameter at a time
        kwargs = {"Ktrans": 0.6, "ve": 0.2, "vp": 0.3, "Ta": 30.0}
        kwargs[param] = value
        osipi.extended_tofts(time_array, aif, **kwargs)


# Tests for the 2CXM model


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


@pytest.mark.parametrize(
    "param, value, match",
    [
        ("Fp", [10], "numeric scalar"),  # Non-scalar Fp
        ("PS", "five", "numeric scalar"),  # Non-numeric PS
        ("ve", np.array([0.2]), "numeric scalar"),  # Array ve
        ("vp", None, "numeric scalar"),  # None value
        ("Fp", -5, "positive"),  # Negative Fp
        ("PS", -1, "non-negative"),  # Negative PS
        ("ve", -0.1, "in range \[0, 1\]"),  # ve < 0
        ("vp", 1.1, "in range \[0, 1\]"),  # vp > 1
        (("ve", "vp"), (0.8, 0.3), "Sum of ve \(0.8\) and vp \(0.3\) exceeds 1"),
    ],
    ids=[
        "Fp_type",
        "PS_type",
        "ve_type",
        "vp_type",
        "Fp_negative",
        "PS_negative",
        "ve_range",
        "vp_range",
        "ve_vp_sum",
    ],
)
def test_2cxm_invalid_inputs(time_array, aif, param, value, match):
    """Test invalid parameter values/type for all model parameters"""
    with pytest.raises((ValueError, TypeError), match=match):
        # Construct kwargs with default valid values
        kwargs = {"Fp": 10, "PS": 5, "ve": 0.2, "vp": 0.1}
        # Handle tuple parameters for combined validation case
        if isinstance(param, tuple):
            for p, v in zip(param, value):
                kwargs[p] = v
        else:
            kwargs[param] = value
        osipi.two_compartment_exchange_model(time_array, aif, **kwargs)


if __name__ == "__main__":
    pytest.main([__file__])
