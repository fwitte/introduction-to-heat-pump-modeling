
from CoolProp.CoolProp import PropsSI
import numpy as np
import pandas as pd


def generate_pvT_input_data(fluid, p_min, p_max, t_max, d_min, d_max):
    p_crit = PropsSI("PCRIT", fluid)
    p_range_two_phase = np.geomspace(p_min, p_crit)

    bubble_vol = 1 / PropsSI("D", "P", p_range_two_phase, "Q", 0, fluid)
    bubble_temp = PropsSI("T", "P", p_range_two_phase, "Q", 0, fluid) - 273.15
    dew_vol = 1 / PropsSI("D", "P", p_range_two_phase, "Q", 1, fluid)
    dew_temp = PropsSI("T", "P", p_range_two_phase, "Q", 1, fluid) - 273.15

    two_phase_temp = pd.DataFrame()
    two_phase_vol = pd.DataFrame()
    for Q in np.linspace(0, 1, 10):
        two_phase_temp[Q] = PropsSI("T", "P", p_range_two_phase, "Q", Q, fluid) - 273.15
        two_phase_vol[Q] = 1 / PropsSI("D", "P", p_range_two_phase, "Q", Q, fluid)

    p_range_subcooled = p_range_two_phase
    p_range_subcooled[-1] *= 0.99999999

    subcooled_temp = pd.DataFrame()
    subcooled_vol = pd.DataFrame()
    for p in p_range_subcooled:
        for i, d in enumerate(np.geomspace(d_min, PropsSI("D", "P", p, "Q", 0, fluid))):
            subcooled_temp.loc[i, p] = PropsSI("T", "P", p, "D", d, fluid) - 273.15
            subcooled_vol.loc[i, p] = 1 / d

    p_range_overheated = p_range_subcooled

    overheated_temp = pd.DataFrame()
    overheated_vol = pd.DataFrame()
    for p in p_range_overheated:
        for i, d in enumerate(np.geomspace(PropsSI("D", "P", p, "Q", 1, fluid), d_max)):
            overheated_temp.loc[i, p] = PropsSI("T", "P", p, "D", d, fluid) - 273.15
            overheated_vol.loc[i, p] = 1 / d

    mask = overheated_temp >= t_max
    overheated_temp[mask] = np.nan

    p_range_supercritical = np.geomspace(p_crit * 1.000001, p_max, 5)
    d_range = np.geomspace(d_min, d_max)
    supercritical_temp = pd.DataFrame()
    supercritical_vol = pd.DataFrame()
    for p in p_range_supercritical:
        supercritical_temp[p] = PropsSI("T", "P", p, "D", d_range, fluid) - 273.15
        supercritical_vol[p] = 1 / d_range

    mask = supercritical_temp >= t_max
    supercritical_temp[mask] = np.nan
    supercritical_vol[mask] = np.nan
    first_missing = pd.isna(overheated_temp).idxmax()

    for p in first_missing.index:
        i = first_missing[p]
        if i > 0:
            overheated_temp.loc[i, p] = t_max
            overheated_vol.loc[i, p] = 1 / PropsSI("D", "P", p, "T", t_max + 273.15, fluid)

    first_missing = pd.isna(supercritical_temp).idxmax()

    for p in first_missing.index:
        i = first_missing[p]
        if i > 0:
            supercritical_temp.loc[i, p] = t_max
            supercritical_vol.loc[i, p] = 1 / PropsSI("D", "P", p, "T", t_max + 273.15, fluid)

    data = {
        "supercritical": {
            "T": supercritical_temp,
            "v": supercritical_vol,
            "p": p_range_supercritical
        },
        "subcooled": {
            "T": subcooled_temp,
            "v": subcooled_vol,
            "p": p_range_subcooled
        },
        "overheated": {
            "T": overheated_temp,
            "v": overheated_vol,
            "p": p_range_overheated
        },
        "twophase": {
            "T": two_phase_temp,
            "v": two_phase_vol,
            "p": p_range_two_phase
        },
        "dewline": {
            "T": dew_temp,
            "v": dew_vol,
            "p": p_range_two_phase
        },
        "bubbleline": {
            "T": bubble_temp,
            "v": bubble_vol,
            "p": p_range_two_phase
        }
    }
    return data


fluid = "NH3"
t_min = -25
t_max = 150
print(PropsSI("P", "T", t_min + 273.15, "Q", 0, fluid))
print(PropsSI("PCRIT", fluid))
p_min = 1.5e5
p_max = 200e5
d_min = PropsSI("D", "Q", 0, "P", p_min, fluid)
d_max = PropsSI("D", "Q", 1, "P", p_min, fluid)
data = generate_pvT_input_data(fluid, p_min, p_max, t_max, d_min, d_max)

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as mticker


def log_tick_formatter(val, pos=None):
    return f"$10^{{{int(val)}}}$"


fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(projection='3d'))

ax.zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
ax.xaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
ax.zaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))


bl = data["bubbleline"]
ax.plot(np.log10(bl["v"]), bl["T"], np.log10(bl["p"]), color="r")

dl = data["dewline"]
ax.plot(np.log10(dl["v"]), dl["T"], np.log10(dl["p"]), color="r")

tp = data["twophase"]
for i, p in enumerate(tp["p"]):
    ax.plot(np.log10(tp["v"].loc[i]), tp["T"].loc[i], np.log10(np.array([p] * len(tp["T"].columns))), color="r")

sc = data["subcooled"]
for i, p in enumerate(sc["p"]):
    ax.plot(np.log10(sc["v"][p]), sc["T"][p], np.log10(np.array([p] * len(sc["p"]))), color="b")

oh = data["overheated"]
for i, p in enumerate(oh["p"]):
    ax.plot(np.log10(oh["v"][p]), oh["T"][p], np.log10(np.array([p] * len(oh["T"].index))), color="c")

sc = data["supercritical"]
for i, p in enumerate(sc["p"]):
    ax.plot(np.log10(sc["v"][p]), sc["T"][p], np.log10(np.array([p] * len(sc["T"].index))), color="y")

ax.set_xlabel("specific volume $v$ in m$^3$/kg")
ax.set_ylabel("temperature $T$ in °C")
ax.set_zlabel("pressure $p$ in bar")
ax.set_ylim([t_min, t_max])
ax.view_init(azim=315)
plt.tight_layout()
plt.savefig(f"pvT_{fluid}.svg", bbox_inches='tight')
plt.savefig(f"pvT_{fluid}.png", bbox_inches='tight')
frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
ax.set_xlabel("")

ax.view_init(azim=360, elev=0)
plt.tight_layout()
plt.savefig(f"pT_{fluid}.svg", bbox_inches='tight')
plt.savefig(f"pT_{fluid}.png", bbox_inches='tight')
