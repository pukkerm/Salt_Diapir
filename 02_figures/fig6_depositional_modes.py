# ---------------------------------------------------------------------------
# Paths for the public data-and-code release (added by the release-packaging pass).
# Raw Badlands outputs are read from BADLANDS_OUTPUT; the derived data used by
# these scripts read the derived data from the release's derived-data folder.
# ---------------------------------------------------------------------------
import os as _os
import glob as _glob


def _release_root(start):
    d = _os.path.dirname(_os.path.abspath(start))
    while d and d != _os.path.dirname(d):
        if _glob.glob(_os.path.join(d, '*_derived_data')):
            return d
        d = _os.path.dirname(d)
    return _os.path.dirname(_os.path.abspath(start))


def _release_dir(name):
    """Locate a numbered release folder (for example 03_derived_data) by pattern."""
    hits = sorted(_glob.glob(_os.path.join(ROOT_DIR, name)))
    return hits[0] if hits else None


ROOT_DIR = _release_root(__file__)
EXTRACT = _os.environ.get('EXTRACT_DIR', _release_dir('*_derived_data') or _os.path.join(ROOT_DIR, '03_derived_data'))
RAW = _os.environ.get('BADLANDS_OUTPUT', _os.path.join(ROOT_DIR, 'raw_badlands_output'))

# -*- coding: utf-8 -*-
"""Figure 6 - three depositional modes of a canyon-fed turbidity current against a pre-existing diapir."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import set_style, outdir
# --- explicit publication settings (audited by nature-figure validate_figure.py) ---
import matplotlib as mpl
try:
    from audit_panel_alignment import require_matplotlib_panel_alignment
except Exception:  # optional layout audit; not required to reproduce the figure
    def require_matplotlib_panel_alignment(*args, **kwargs):
        return None
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'Liberation Sans', 'DejaVu Sans']
mpl.rcParams.update({
    'svg.fonttype': 'none',
    'pdf.fonttype': 42,
})


set_style(7.0)
SUB, LEV, LEV_L, RED = '#d6d6d6', '#f6c98b', '#8a4b12', '#c00000'
KIND = ['unconf', 'inter', 'bypass']
SEC = ['A', 'B', 'C']
TITLE = ['(a) Unconfined levee development',
         '(b) Confined levee: partial deflection',
         '(c) Confined levee: bypass and axial starvation']
H = [0.030, 0.170, 0.255]

def mode(ax, kind, h, tag):
    x = np.linspace(0, 1, 600)
    assert np.all(np.diff(x) > 0), 'np.interp requires an increasing grid'
    base = 0.42 - 0.070 * x + h * np.exp(-((x - 0.68) / 0.115) ** 2)
    ax.fill_between(x, 0.0, base, fc=SUB, ec='none', zorder=1)
    ax.plot(x, base, color='k', lw=0.9, zorder=3)
    cfg = {'unconf': (0.22, 0.135, 0.40, 0.97), 'inter': (0.22, 0.195, 0.30, 0.72), 'bypass': (0.22, 0.215, 0.26, 0.64)}[kind]
    x0, T0, dec, x1 = cfg
    xs = x[(x >= x0) & (x <= x1)]
    T = T0 * np.exp(-(xs - x0) / dec) * np.clip((xs - x0) / 0.06, 0, 1)
    bs = np.interp(xs, x, base); top = bs + T
    ax.fill_between(xs, bs, top, fc=LEV, ec='none', zorder=4)
    for f in [0.0, 0.25, 0.5, 0.75, 1.0]:
        ax.plot(xs, bs + f * T, color=LEV_L if f in (0.0, 1.0) else '#b06a1f', lw=0.8 if f in (0.0, 1.0) else 0.4, zorder=5)
    if kind == 'inter':
        xt = x[(x >= 0.72) & (x <= 1.0)]
        bt = np.interp(xt, x, base); Tt = 0.030 * np.exp(-(xt - 0.72) / 0.32)
        ax.fill_between(xt, bt, bt + Tt, fc=LEV, ec='none', zorder=4)
        for f in [0.0, 0.5, 1.0]:
            ax.plot(xt, bt + f * Tt, color=LEV_L if f in (0.0, 1.0) else '#b06a1f', lw=0.6 if f in (0.0, 1.0) else 0.35, zorder=5)
    if kind == 'bypass':
        xr = x[(x >= 0.84)]
        br = np.interp(xr, x, base); Tr = 0.050 * np.exp(-(xr - 0.84) / 0.13)
        ax.fill_between(xr, br, br + Tr, fc=LEV, ec='none', zorder=4)
        for f in [0.0, 0.5, 1.0]:
            ax.plot(xr, br + f * Tr, color=LEV_L if f in (0.0, 1.0) else '#b06a1f', lw=0.7 if f in (0.0, 1.0) else 0.4, zorder=5)
    for xa in np.linspace(xs[0] + 0.03, xs[-1] - 0.12, 4):
        ya = float(np.interp(xa, xs, bs)); xb = min(xa + 0.06, xs[-1])
        ax.add_patch(FancyArrowPatch((xa, ya + 0.005), (xb, float(np.interp(xb, xs, bs)) + 0.005),
                                     arrowstyle='-|>', mutation_scale=5.5, lw=0.9, color=RED, zorder=7))
    ax.text(0.004, 0.30, tag, fontsize=7.0, va='center', zorder=10)
    ax.text(0.996, 0.30, tag + '1', fontsize=7.0, va='center', ha='right', zorder=10)
    ax.text(0.012, 0.955, TITLE[SEC.index(tag)], transform=ax.transAxes, fontsize=6.6, va='top', zorder=10)
    def lead(txt, xy, xyt, fs=5.6):
        ax.annotate(txt, xy=xy, xytext=xyt, fontsize=fs, color='k', zorder=10,
                    arrowprops=dict(arrowstyle='-', color='0.15', lw=0.5, shrinkA=1, shrinkB=1))
    if kind == 'unconf':
        lead('Wedge-shaped levee deposit', (0.46, float(np.interp(0.46, xs, bs)) + 0.055), (0.30, 0.80))
        lead('Downlap onto the pre-existing surface', (0.90, float(np.interp(0.90, xs, bs)) + 0.012), (0.55, 0.14))
        ax.text(0.30, 0.045, 'Pre-existing structural surface', fontsize=5.4, color='0.25', zorder=10)
    elif kind == 'inter':
        lead('Confined levee geometry', (0.44, float(np.interp(0.44, xs, bs)) + 0.075), (0.28, 0.82))
        lead('Onlap onto the flank of the structure', (0.70, float(np.interp(0.70, xs, bs)) + 0.010), (0.52, 0.16))
        ax.text(0.30, 0.045, 'Pre-existing structural surface', fontsize=5.4, color='0.25', zorder=10)
    else:
        lead('Confined levee wedge', (0.42, float(np.interp(0.42, xs, bs)) + 0.085), (0.24, 0.84))
        lead('Crest thinning', (0.70, float(np.interp(0.70, xs, bs)) + 0.085), (0.56, 0.80))
        lead('Detached bypass lobe', (0.90, float(np.interp(0.90, xr, br)) + 0.020), (0.05, 0.60))
        ax.text(0.30, 0.045, 'Pre-existing structural surface', fontsize=5.4, color='0.25', zorder=10)
    ia = ax.inset_axes([0.735, 0.52, 0.255, 0.42])
    ia.add_patch(Ellipse((0.56, 0.50), 0.26, 0.66, fc='#f0d5a6', ec=LEV_L, lw=0.7, ls=(0, (3, 2)), zorder=3))
    ia.plot([0.03, 0.97], [0.50, 0.50], color='k', lw=0.5, ls=(0, (5, 3)), zorder=4)
    ia.text(0.03, 0.56, tag, fontsize=5.0, zorder=5)
    ia.text(0.97, 0.56, tag + '1', fontsize=5.0, ha='right', zorder=5)
    ia.text(0.56, 0.03, 'diapir', fontsize=5.0, ha='center', va='bottom', color=LEV_L, zorder=5)
    if kind == 'unconf':
        ia.add_patch(FancyArrowPatch((0.04, 0.42), (0.96, 0.50), arrowstyle='-|>', mutation_scale=5, lw=1.1, color='#1f4e79', zorder=6))
    elif kind == 'inter':
        ia.add_patch(FancyArrowPatch((0.04, 0.40), (0.94, 0.86), connectionstyle='arc3,rad=-0.28', arrowstyle='-|>', mutation_scale=5, lw=1.0, color='#1f4e79', zorder=6))
        ia.add_patch(FancyArrowPatch((0.04, 0.40), (0.94, 0.14), connectionstyle='arc3,rad=0.28', arrowstyle='-|>', mutation_scale=5, lw=1.0, color='#1f4e79', zorder=6))
    else:
        ia.add_patch(FancyArrowPatch((0.03, 0.38), (0.95, 0.94), connectionstyle='arc3,rad=-0.44', arrowstyle='-|>', mutation_scale=5.5, lw=1.2, color='#1f4e79', zorder=6))
        ia.add_patch(FancyArrowPatch((0.03, 0.38), (0.95, 0.06), connectionstyle='arc3,rad=0.44', arrowstyle='-|>', mutation_scale=5.5, lw=1.2, color='#1f4e79', zorder=6))
    ia.set_xlim(0, 1); ia.set_ylim(0, 1); ia.set_xticks([]); ia.set_yticks([])
    for sp in ia.spines.values():
        sp.set_linewidth(0.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc='none', ec='0.35', lw=0.7, transform=ax.transAxes, zorder=11, clip_on=False))

fig = plt.figure(figsize=(7.09, 5.6))
gs = fig.add_gridspec(3, 1, hspace=0.14, left=0.015, right=0.985, top=0.985, bottom=0.015)
for i in range(3):
    ax = fig.add_subplot(gs[i, 0])
    mode(ax, KIND[i], H[i], SEC[i])
od = outdir('fig6')
FIG6 = os.path.join(od, 'Figure6_depositional_modes')
# schematic rows carry their own in-panel mode titles, so panel letters are not required
require_matplotlib_panel_alignment(
    fig, json_out=FIG6 + '.alignment.json', overlay_svg=FIG6 + '.alignment.svg',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=False)
fig.savefig(FIG6 + '.pdf')
fig.savefig(FIG6 + '.svg')
fig.savefig(FIG6 + '.png', dpi=600)
fig.savefig(FIG6 + '.tiff', dpi=600)
print('saved', FIG6, flush=True)
plt.close(fig)
print('DONE')
