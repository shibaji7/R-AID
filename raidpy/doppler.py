#!/usr/bin/env python

"""doppler.py: Doppler is dedicated to doppler related function."""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

from dataclasses import dataclass

import numpy as np
import pandas as pd
from loguru import logger
from scipy.signal import resample

from raidpy.constants import *


@dataclass
class Doppler:
    mode: str = None
    wave_disp_reltn_form: str = None
    pt0: pd.DataFrame = None
    pt1: pd.DataFrame = None


class ComputeDoppler(object):
    """
    This class is used to Doppler height profile.

    pt0 = Phase at time t0
    pt1 = Phase at time t1
    del_t = Total time in secs
    fo = operating frequency
    """

    def __init__(
        self,
        pt0: pd.DataFrame,
        pt1: pd.DataFrame,
        fo: float,
        del_t: float,
        _run_=False,
        mode: str = "O",
        wave_disp_reltn_form: str = "",
        dop_analy: dict = dict(
            n_sample=1000,
        ),
    ):
        self.pt0 = pt0
        self.pt1 = pt1
        self.fo = fo
        self.del_t = del_t
        self.wave_disp_reltn_form = wave_disp_reltn_form
        self.mode = mode
        self.dop_analy = dop_analy
        self.w = 2 * np.pi * fo
        self.k = (2 * np.pi * fo) / pconst["c"]
        if _run_:
            logger.info(f"Running Doppler calculations....")
            self.estimate_dop()
        return

    def estimate_dop(self):
        self.dop = Doppler(
            pt0=self.pt0,
            pt1=self.pt1,
            mode=self.mode,
            wave_disp_reltn_form=self.wave_disp_reltn_form,
        )
        logger.info(
            f"Solving Doppler for {self.wave_disp_reltn_form.upper()} Mode>{self.mode}"
        )
        print(self.pt0.head(), self.pt1.head())
        # p0, p1 = (
        #     getattr(
        #         self.pt0,
        #         f"mode_{self.mode}",
        #     ),
        #     getattr(
        #         self.pt1,
        #         f"mode_{self.mode}",
        #     ),
        # )
        # p0_resample, p1_resample = (
        #     resample(p0, self.dop_analy["n_sample"]),
        #     resample(p1, self.dop_analy["n_sample"]),
        # )
        # print(p0, p0_resample)
        # dp, df = (
        #     (p1_resample - p0_resample) / self.del_t,
        #     (p1_resample - p1_resample) / (self.del_t * 4 * np.pi),
        # )
        # dv = df * pconst["c"] / (2 * self.fo)
        return


class ComputeKikuchiDoppler(object):
    """
    This class is used to Kikuchi's Doppler height profile.

    df0 = Details at time t0
    df1 = Details at time t1
    del_t = Total time in secs
    fo = operating frequency
    """

    def __init__(
        self,
        pt0: pd.DataFrame,
        pt1: pd.DataFrame,
        fo: float,
        del_t: float,
        _run_=False,
    ):
        return
