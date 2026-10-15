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
"""Revised Figure 2 - plan-view cumulative sediment thickness for five diapir heights.

Outputs: composite PNG/PDF/SVG/TIFF, one file per panel (for CorelDRAW assembly),
a standalone colour bar, and the render-time panel-alignment report.

Panel geometry is set explicitly (identical panel size and identical gutters in
both directions) so the alignment gate can be satisfied by construction.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
try:
    from audit_panel_alignment import require_matplotlib_panel_alignment
except Exception:  # optional layout audit; not required to reproduce the figure
    def require_matplotlib_panel_alignment(*args, **kwargs):
        return None

C.set_style(7.0)
# --- explicit publication settings (audited by nature-figure validate_figure.py) ---
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'Liberation Sans', 'DejaVu Sans']
mpl.rcParams.update({
    'svg.fonttype': 'none',
    'pdf.fonttype': 42,
})

OUT = C.outdir('fig2')
PAN = os.path.join(OUT, 'panels'); os.makedirs(PAN, exist_ok=True)

xi = np.load(os.path.join(C.EXTRACT, 'xi.npy')) / 1000.0
yi = np.load(os.path.join(C.EXTRACT, 'yi.npy')) / 1000.0
XLIM, YLIM, VMAX = (130.0, 200.0), (65.0, 135.0), 200.0
ix = np.where((xi >= XLIM[0]) & (xi <= XLIM[1]))[0]
iy = np.where((yi >= YLIM[0]) & (yi <= YLIM[1]))[0]
EXT = [xi[ix[0]], xi[ix[-1]], yi[iy[0]], yi[iy[-1]]]
STEPS = [10, 20, 30]
CMAP = 'cividis'


def load(ts, case):
    return np.load(os.path.join(C.EXTRACT, 'T_step%02d_%s.npy' % (ts, case)))[np.ix_(iy, ix)]


def draw(ax, T, case, letter=None, ticks=True):
    im = ax.imshow(T, extent=EXT, origin='lower', cmap=CMAP,
                   norm=Normalize(0, VMAX), interpolation='bilinear', aspect='auto')
    C.diapir_footprint(ax, color='w', lw=0.7,
                       ls='--' if case != 'fan' else (0, (1.0, 1.3)))
    C.canyon_mouth(ax, color='w')
    if letter:
        C.panel_letter(ax, letter, color='w', loc='left')
    ax.set_xlim(XLIM); ax.set_ylim(YLIM)
    ax.set_xticks([140, 160, 180, 200]); ax.set_yticks([80, 100, 120])
    if not ticks:
        ax.set_xticklabels([]); ax.set_yticklabels([])
    return im


# ---------------- composite ----------------
FWMM, FHMM = 180.0, 122.0          # page size
PWMM, PHMM = 29.80, 29.80          # panel size (square)
LMM, BMM = 14.00, 18.66            # left / bottom margin
GXMM, GYMM = 3.00, 5.43            # horizontal / vertical gutter
fig = plt.figure(figsize=(7.087, 4.803))   # 180 x 122 mm
axes = np.empty((3, 5), dtype=object)
for r in range(3):
    for c in range(5):
        axes[r, c] = fig.add_axes([(LMM + c * (PWMM + GXMM)) / FWMM,
                                   (BMM + (2 - r) * (PHMM + GYMM)) / FHMM,
                                   PWMM / FWMM, PHMM / FHMM])
last = None
for r, ts in enumerate(STEPS):
    for c, case in enumerate(C.CASES):
        ax = axes[r, c]
        last = draw(ax, load(ts, case), case,
                    letter=chr(ord('a') + r * 5 + c),
                    ticks=(r == 2 or c == 0))
        if r == 2:
            ax.set_xlabel('X (km)', labelpad=1.0)
        if c == 0:
            ax.set_ylabel('Y (km)', labelpad=1.0)
        if r == 0:
            ax.set_title(C.TITLE[case], pad=2.0)
        if r < 2:
            ax.set_xticklabels([])
        if c > 0:
            ax.set_yticklabels([])
cax = fig.add_axes([0.2937, 0.0506, 0.4614, 0.0145])
cb = fig.colorbar(last, cax=cax, orientation='horizontal')
cb.set_label('Cumulative sediment thickness (m)', labelpad=1.5)
cb.set_ticks([0, 50, 100, 150, 200]); cb.ax.tick_params(width=0.6, length=2.0)
for r, ts in enumerate(STEPS):
    b = axes[r, 0].get_position()
    t = fig.text(0.010, 0.5 * (b.y0 + b.y1), '%d kyr (Step %d)' % (C.STEPS[ts], ts),
                 rotation=90, rotation_mode='anchor', va='center', ha='center', fontsize=7)
    t.set_in_layout(False)

PANEL_ID = {axes[r, c]: chr(ord('a') + r * 5 + c) for r in range(3) for c in range(5)}
ROW_GROUPS = [[chr(ord('a') + r * 5 + c) for c in range(5)] for r in range(3)]
COL_GROUPS = [[chr(ord('a') + r * 5 + c) for r in range(3)] for c in range(5)]
FIG2 = os.path.join(OUT, 'Figure2_thickness_maps')
require_matplotlib_panel_alignment(
    fig, json_out=FIG2 + '.alignment.json', overlay_svg=FIG2 + '.alignment.svg',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=True,
    panel_ids=PANEL_ID, row_groups=ROW_GROUPS, column_groups=COL_GROUPS,
    exclude_axes=[cb.ax])
fig.savefig(FIG2 + '.pdf')
fig.savefig(FIG2 + '.svg')
fig.savefig(FIG2 + '.png', dpi=600)
fig.savefig(FIG2 + '.tiff', dpi=600)
print('saved composite', flush=True)
C.plt_close(fig)

# ---------------- individual panels ----------------
for r, ts in enumerate(STEPS):
    for c, case in enumerate(C.CASES):
        f, ax = plt.subplots(figsize=(48 * C.MM, 46 * C.MM))
        m = draw(ax, load(ts, case), case)
        ax.set_xlabel('X (km)', labelpad=1.0)
        ax.set_ylabel('Y (km)', labelpad=1.0)
        ax.set_title('%d kyr (Step %d), %s' % (C.STEPS[ts], ts, C.TITLE[case][1:-1]), pad=2.0)
        f.savefig(os.path.join(PAN, 'panel_%s_step%02d.png' % (case, ts)), dpi=600)
        f.savefig(os.path.join(PAN, 'panel_%s_step%02d.pdf' % (case, ts)))
        f.savefig(os.path.join(PAN, 'panel_%s_step%02d.svg' % (case, ts)))
        C.plt_close(f)
print('saved %d panels' % (len(STEPS) * len(C.CASES)), flush=True)

# ---------------- standalone colour bar ----------------
f, ax = plt.subplots(figsize=(70 * C.MM, 10 * C.MM))
cb = f.colorbar(plt.cm.ScalarMappable(norm=Normalize(0, VMAX), cmap=CMAP), cax=ax,
                orientation='horizontal', ticks=[0, 50, 100, 150, 200])
cb.set_label('Cumulative sediment thickness (m)')
f.savefig(os.path.join(PAN, 'colorbar_thickness.png'), dpi=600)
f.savefig(os.path.join(PAN, 'colorbar_thickness.pdf'))
f.savefig(os.path.join(PAN, 'colorbar_thickness.svg'))
print('saved colorbar', flush=True)
