#!/usr/bin/env python

"""functions.py: Calculate absorption along the path"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

import datetime as dt
import os

import numpy as np
import pandas as pd
from loguru import logger

from raidpy import utils
from raidpy.iono import Ionosphere2d
from raidpy.plots import PlotOlRays


class Oblique(object):
    """
    This class takes PHaRLAP rays as input and computes absorption along the path
    """

    def __init__(
        self,
        date: dt.datetime,
        grange: np.array,
        height: np.array,
        ray_bearing: float,
        origin_lat: float,
        origin_lon: float,
        fo: float,
        ion2d: dict = None,
        igrf2d: dict = None,
        msise: dict = None,
        edens: np.array = None,
    ):
        self.date = date
        self.grange = grange
        self.height = height
        self.ray_bearing = ray_bearing
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        self.edens = edens
        self.fo = fo
        self.ion2d = ion2d
        self.igrf2d = igrf2d
        self.initialize()
        return

    def initialize(self):
        logger.info(f"Initialize for {self.date}")
        self.glats, self.glons = utils.create_lat_lon_from_routes(
            self.grange, self.ray_bearing, self.origin_lat, self.origin_lon
        )
        self.galts = np.array(self.height)
        self.iono = Ionosphere2d(self.date, self.glats, self.glons, self.galts, self.fo)
        if self.edens is not None:
            logger.info(f"change e-dens")
            self.iono.iri_block.iri["edens"] = self.edens
        self.iono.compute()
        self.ray = pd.DataFrame()
        self.ray["grange"], self.ray["height"] = self.grange, self.height
        return

    def plot_absorption(
        self,
        phase_path: np.array,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
        fig_path: str = "figures/test_figures.png",
        text: str = None,
    ):
        logger.info(f"Plotting for {self.date} for {wave_disp_reltn}:{col_freq}")
        pol = PlotOlRays(self.date)
        self.ray["abs"] = getattr(
            getattr(getattr(self.iono.ca, wave_disp_reltn), col_freq), f"mode_{mode}"
        )
        o = self.ray.copy().fillna(0)
        total_absorption = np.trapz(o["abs"], phase_path)
        logger.info(f"Total absorption {total_absorption} dB")
        pol.lay_rays(self.ray, text=text + r" / $\int\beta$=%.1f dB" % total_absorption)
        dirc = fig_path.split("/")
        if len(dirc) > 1:
            os.makedirs("/".join(dirc[:-1]), exist_ok=True)
        pol.save(fig_path)
        pol.close()
        logger.info(f"Saving files in {fig_path}")
        return


if __name__ == "__main__":
    bearing_file_loc = "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_05MHz_SCurve/2024-04-08/wwv/sami3/w2naf/bearing.mat"
    bearing = utils.load_bearing_mat_file(bearing_file_loc)
    rays_file_loc = "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_05MHz_SCurve/2024-04-08/wwv/sami3/w2naf/1700_rt.mat"
    elv = 12
    _, rays = utils.load_rays_mat_file(rays_file_loc)
    ray = rays[elv]
    ol = Oblique(
        dt.datetime(2024, 4, 8, 17),
        np.array(ray.ground_range),
        np.array(ray.height),
        bearing.rb,
        bearing.olat,
        bearing.olon,
        bearing.freq.ravel().tolist()[0] * 1e6,
        edens=np.array(ray.electron_density) * 1e6,  # To /m3
    )
    ol.plot_absorption(
        np.array(ray.phase_path),
        wave_disp_reltn="ah",
        col_freq="av_mb",
        text=r"Spot: wwv-w2naf / 5 Mhz, $\alpha=12^\circ$ / $\beta=\beta_{ah}(\nu_{av-mb})$",
    )
