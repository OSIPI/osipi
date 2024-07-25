#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: eveshalom
"""

import numpy as np


def createR10_withref(S0ref, S0, Tr, fa, T1ref, datashape):
    R10_ref = 1 / T1ref
    ref_frac = (1 - np.cos(fa) * np.exp(-Tr * R10_ref)) / (1 - np.exp(-Tr * R10_ref))
    R10 = (-1 / Tr) * np.log((S0 - (ref_frac * S0ref)) / ((S0 * np.cos(fa)) - (ref_frac * S0ref)))
    R10 = np.tile(R10[:, :, :, np.newaxis], (1, 1, 1, datashape[-1]))
    return R10


def calcR1_R2(R10, R20st, r1, r2st, Ctiss):
    R1 = R10 + r1 * Ctiss
    R2st = R20st + r2st * Ctiss
    return R1, R2st


def Conc2Sig_Linear(Tr, Te, fa, R1, R2st, S, scale, scalevisit1):
    dro_S = ((1 - np.exp(-Tr * R1)) / (1 - (np.cos(fa) * np.exp(-Tr * R1)))) * (
        np.sin(fa) * np.exp(-Te * R2st)
    )

    if scale == 1:
        ScaleConst = np.percentile(S, 98) / np.percentile(dro_S, 98)
    elif scale == 2:
        ScaleConst = scalevisit1

    dro_S = dro_S * ScaleConst
    return dro_S, ScaleConst


def STDmap(S, t0):
    stdev = np.std(S[:, :, :, 0:t0], axis=3)
    return stdev


def addnoise(a, std, Sexact, Nt):
    from numpy.random import normal as gaussian

    std = np.tile(std[:, :, :, np.newaxis], (1, 1, 1, Nt))
    Snoise = abs(Sexact + (a * std * gaussian(0, 1, Sexact.shape)))
    return Snoise
