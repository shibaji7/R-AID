#!/usr/bin/env python

"""oblique.py: Calculate absorption along the oblique path"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

import numpy as np

from raidpy import utils


class Oblique(object):
    """
    This class takes PHaRLAP rays as input and computes absorption along the path
    """

    def __init__(
        self,
        grange: np.array,
        height: np.array,
        ion2d: dict,
        igrf2d: dict,
    ):
        self.grange = grange
        self.height = height
        self.ion2d = ion2d
        self.igrf2d = igrf2d
        # self.
        return


if __name__ == "__main__":
    bearing_file_loc = "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_05MHz_SCurve/2024-04-08/wwv/sami3/w2naf/bearing.mat"
    bearing = utils.load_bearing_mat_file(bearing_file_loc)
    rays_file_loc = "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_05MHz_SCurve/2024-04-08/wwv/sami3/w2naf/1700_rt.mat"
    rays = utils.load_rays_mat_file(rays_file_loc)
    pass
