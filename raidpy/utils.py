#!/usr/bin/env python

"""utils.py: Calculate all the functions of utility"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

from types import SimpleNamespace

import numpy as np
import pandas as pd
from loguru import logger
from scipy.io import loadmat


def load_bearing_mat_file(file_loc: str):
    logger.info(f" Loading bearing file: {file_loc}")
    bearing = SimpleNamespace(**loadmat(file_loc))
    return bearing


def load_rays_mat_file(file_loc: str):
    logger.info(f" Loading rays file: {file_loc}")
    sim_data = loadmat(file_loc)
    path_data_keys = [
        "ground_range",
        "height",
        "group_range",
        "phase_path",
        "geometric_distance",
        "electron_density",
        "refractive_index",
    ]
    ray_data_keys = [
        "ground_range",
        "group_range",
        "phase_path",
        "geometric_path_length",
        "initial_elev",
        "final_elev",
        "apogee",
        "gnd_rng_to_apogee",
        "plasma_freq_at_apogee",
        "virtual_height",
        "effective_range",
        "deviative_absorption",
        "TEC_path",
        "Doppler_shift",
        "Doppler_spread",
        "frequency",
        "nhops_attempted",
        "ray_label",
    ]
    ray_data = []
    for i in range(sim_data["ray_data"].shape[1]):
        r_data = dict()
        for key in ray_data_keys:
            r_data[key] = sim_data["ray_data"][0, i][key].ravel()[0]
        ray_data.append(r_data)
    rays = pd.DataFrame.from_records(ray_data)
    return rays


def create_lat_lon_from_routes(
    grange: np.array,
    height: np.array,
    bearing: float = None,
    source: dict = dict(),
    target: dict = dict(),
):

    return
