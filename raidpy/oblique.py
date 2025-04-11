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
    pass
