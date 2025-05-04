import datetime as dt
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from geopy.distance import great_circle as GC
from joblib import Parallel, delayed
from loguru import logger
from tqdm import tqdm

from raidpy import utils
from raidpy.functions import Oblique
from raidpy.plots import PlotOlRays

plt.style.use(["science", "ieee"])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Tahoma", "DejaVu Sans", "Lucida Grande", "Verdana"]
plt.rcParams["text.usetex"] = False


def get_w2naf_dist():
    source = (40.0150, -105.2705)
    target = (41.335116, -75.600692)
    return GC(source, target).km


def create_ol(e, ray, b, d):
    ol = Oblique(
        d,
        np.array(ray.ground_range),
        np.array(ray.height),
        b.rb,
        b.olat,
        b.olon,
        b.freq.ravel().tolist()[0] * 1e6,
        edens=np.array(ray.electron_density) * 1e6,  # To /m3
        ray_details=ray,
    )
    return ol


if __name__ == "__main__":
    import sys

    sys.path.append("Projects/Eclipse2024HamsSCI/py")
    import eclipse_plots as ep

    wave_disp_reltn, col_freq, mode = "ah", "sn", "O"
    dist = get_w2naf_dist()
    n_jobs = 30
    dates = [
        dt.datetime(2024, 4, 8, 17) + dt.timedelta(minutes=i * 5) for i in range(1)
    ]
    nhop, tfreq = 2, 10
    folder = os.path.join(
        "/home/chakras4/OneDrive/trace/outputs/",
        "GAE2024_SAMI3_w2naf_%02dHop_%02dMHz/" % (nhop, tfreq),
        "2024-04-08/wwv/sami3/w2naf/",
    )
    bearing_file_loc = os.path.join(folder, "bearing.mat")
    bearing = utils.load_bearing_mat_file(bearing_file_loc)
    tfreq = bearing.freq.ravel()[0]
    logger.info(f"tFreq: {tfreq}")

    phase = dict(
        ah_sn=[],
        sw_ft=[],
        ah_mb=[],
        ah_cc=[],
    )
    dirc = f"figures/2024GAE/phase/{tfreq}_{nhop}"

    for d in dates:
        logger.info(f"Date: {d}")
        floc = os.path.join(folder, f"{d.strftime('%H%M')}_rt.mat")
        _, rays = utils.load_rays_mat_file(floc)
        elvs = []
        for e in list(rays.keys()):
            ground_range = rays[e].ground_range.iloc[-1]
            if np.abs(ground_range - dist) <= 50.0:
                elvs.append(e)
                logger.info(f"Wintin limits: {ground_range} / elv:{e}")
        elvs.sort()

        ols = Parallel(n_jobs=n_jobs)(
            delayed(create_ol)(e, rays[e], b=bearing, d=d) for e in tqdm(elvs)
        )

        phs = np.array(
            [
                [
                    ol.get_total_phase_along_path(None),
                    ol.get_total_phase_along_path(None, "ah", "av_cc"),
                    ol.get_total_phase_along_path(None, "ah", "av_mb"),
                    ol.get_total_phase_along_path(None, "sw", "ft"),
                ]
                for ol in ols
            ]
        )
        phase["ah_sn"].append(np.median(phs[:, 0]))
        phase["ah_cc"].append(np.median(phs[:, 1]))
        phase["ah_mb"].append(np.median(phs[:, 2]))
        phase["sw_ft"].append(np.median(phs[:, 3]))

        if not os.path.exists(dirc + f"/{d.strftime('%H%M')}.png"):
            pl = PlotOlRays(d, ylim=[0, 250], xlim=[0, 3000])
            os.makedirs(dirc, exist_ok=True)
            for i, e, ol in zip(range(len(ols)), elvs, ols):
                ray = ol.get_phase_datasets(wave_disp_reltn, col_freq, mode)
                txt = f"Spot: wwv-w2naf / {tfreq} MHz " + r"/ $\beta=\beta_{ah}(\nu_{sn})$"
                pl.lay_rays(
                    ray,
                    kind="phase",
                    text=txt if i == 0 else "",
                    tag_distance=dist if i == 0 else -1,
                )
            pl.save(dirc + f"/{d.strftime('%H%M')}.png")
            pl.close()
