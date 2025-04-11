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

import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "ieee"])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Tahoma", "DejaVu Sans", "Lucida Grande", "Verdana"]
plt.rcParams["text.usetex"] = False
import mpl_toolkits.axisartist.floating_axes as floating_axes
import numpy as np
from matplotlib.projections import polar
from matplotlib.transforms import Affine2D
from mpl_toolkits.axisartist.grid_finder import DictFormatter, FixedLocator


class PlotOlRays(object):
    def __init__(self, date: dt.datetime, ylim=[], xlim=[]):
        self.date = date
        self.xlim = xlim
        self.ylim = ylim
        return

    def save(self, filepath):
        self.fig.savefig(filepath, bbox_inches="tight", facecolor=(1, 1, 1, 1))
        return

    def close(self):
        self.fig.clf()
        plt.close()
        return

    def get_parameter(self, kind):
        import matplotlib.colors as colors

        if kind == "pf":
            o, cmap, label, norm = (
                getattr(self, kind),
                "plasma",
                r"$f_0$ [MHz]",
                colors.Normalize(
                    self.cfg.ray_trace_plot_lim.pf[0], self.cfg.ray_trace_plot_lim.pf[1]
                ),
            )
        if kind == "edens":
            o, cmap, label, norm = (
                getattr(self, kind),
                "plasma",
                r"$N_e$ [$/cm^{-3}$]",
                colors.LogNorm(
                    self.cfg.ray_trace_plot_lim.edens[0],
                    self.cfg.ray_trace_plot_lim.edens[1],
                ),
            )
        if kind == "ref_indx":
            o, cmap, label, norm = (
                getattr(self, kind),
                "plasma",
                r"$\eta$",
                colors.Normalize(
                    self.cfg.ray_trace_plot_lim.ref_indx[0],
                    self.cfg.ray_trace_plot_lim.ref_indx[1],
                ),
            )
        return o, cmap, label, norm

    def lay_rays(self, kind="pf", zoomed_in=[], elv_range=[], tag_distance: float = -1):
        self.create_figure_pane()

        o, cmap, label, norm = self.get_parameter(kind)
        im = self.ax.pcolormesh(
            self.trace_obj.bearing_object["dist"],
            self.trace_obj.bearing_object["heights"],
            o,
            norm=norm,
            cmap=cmap,
            alpha=0.8,
        )
        pos = self.ax.get_position()
        cpos = [
            pos.x1 + 0.025,
            pos.y0 + 0.05,
            0.015,
            pos.height * 0.6,
        ]
        cax = self.fig.add_axes(cpos)
        cbax = self.fig.colorbar(
            im, cax, spacing="uniform", orientation="vertical", cmap="plasma"
        )
        _ = cbax.set_label(label)
        rays = self.trace_obj.rays
        self.elvs = rays.elvs
        self.elvs = (
            self.elvs
            if (elv_range is None) or (len(elv_range) < 2)
            else self.elvs[(self.elvs >= elv_range[0]) & (self.elvs <= elv_range[1])]
        )
        if tag_distance > 100:
            self.ax.plot(
                [tag_distance, tag_distance],
                [0, 100],
                c="m",
                zorder=4,
                alpha=0.7,
                ls="--",
                lw=0.8,
            )
        for i, elv in enumerate(self.elvs):
            ray_path_data, ray_data = (
                rays.ray_path_data[elv],
                rays.simulation[elv]["ray_data"],
            )
            th, r = (ray_path_data.ground_range.copy(), ray_path_data.height.copy())
            ray_label = ray_data["ray_label"]
            self.ax.plot(th, r, c="k", zorder=3, alpha=0.7, ls="-", lw=0.1)
            col = "k" if ray_label == 1 else "r"
            if ray_label in [-1, 1]:
                self.ax.scatter([th.iloc[-1]], [r.iloc[-1]], marker="s", s=3, color=col)
        stitle = "%s UT" % self.event.strftime("%Y-%m-%d %H:%M")
        self.ax.text(
            0.95, 1.01, stitle, ha="right", va="center", transform=self.ax.transAxes
        )
        stitle = f"Model: {self.cfg.model.upper()} / {self.rad}-{'%02d'%self.beam}, $f_0$={self.cfg.frequency} MHz"
        self.ax.text(
            0.05, 1.02, stitle, ha="left", va="center", transform=self.ax.transAxes
        )

        # Create Zoomed in panel
        if len(zoomed_in):
            self.__zoomed_in_panel__(kind, zoomed_in)
        return

    def create_figure_pane(self):
        self.fig = plt.figure(figsize=(8, 3), dpi=300)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel(r"Height [km]")
        self.ax.set_xlabel(r"Ground range [km]")
        self.ax.set_xlim(
            self.xlim if len(self.xlim) == 2 else [0, self.cfg.max_ground_range_km]
        )
        self.ax.set_ylim(
            self.ylim if len(self.ylim) == 2 else [0, self.cfg.end_height_km]
        )
        return

    def __zoomed_in_panel__(self, kind, zoomed_in):
        self.zoom_ax = self.ax.inset_axes([0.4, 1.3, 0.3, 0.5])
        o, cmap, _, norm = self.get_parameter(kind)
        self.zoom_ax.pcolormesh(
            self.trace_obj.bearing_object["dist"],
            self.trace_obj.bearing_object["heights"],
            o,
            norm=norm,
            cmap=cmap,
            alpha=0.8,
        )
        rays = self.trace_obj.rays
        for i, elv in enumerate(self.elvs):
            ray_path_data, ray_data = (
                rays.ray_path_data[elv],
                rays.simulation[elv]["ray_data"],
            )
            th, r = ray_path_data.ground_range, ray_path_data.height
            self.zoom_ax.plot(th, r, c="k", zorder=3, alpha=0.7, ls="-", lw=0.05)

        self.zoom_ax.set_xlim(zoomed_in[0])
        self.zoom_ax.set_ylim(zoomed_in[1])
        th_ticklabels, r_ticklabels = (
            self.zoom_ax.get_xticklabels(),
            self.zoom_ax.get_yticklabels(),
        )
        self.zoom_ax.set_xlabel("Ground Range, [km]", fontdict={"size": 8})
        self.zoom_ax.set_ylabel("Height, [km]", fontdict={"size": 8})
        self.ax.indicate_inset_zoom(self.zoom_ax)
        return
