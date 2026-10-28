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
"""Figure 5 - controls of diapir relief on sediment routing and mass partitioning."""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.ticker import FuncFormatter, NullFormatter
from common import set_style, outdir, panel_letter
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


EX = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
LAB = ['0 m (Rdf = 0)', '100 m (Rdf = 0.5)', '200 m (Rdf = 1.0)', '250 m (Rdf = 1.25)', '300 m (Rdf = 1.5)']
SHORT = ['Rdf 0', 'Rdf 0.5', 'Rdf 1.0', 'Rdf 1.25', 'Rdf 1.5']
RDF = [0.0, 0.5, 1.0, 1.25, 1.5]
set_style(7.0)
C = plt.get_cmap('cividis')(np.linspace(0.05, 0.92, 5))
MK = ['o', 's', '^', 'D', 'v']
prof = np.load(os.path.join(EX, 'axial_profiles.npz'))
M = json.load(open(os.path.join(EX, 'metrics.json'), encoding='utf-8'))
V = json.load(open(os.path.join(EX, 'volumes.json'), encoding='utf-8'))
VT = json.load(open(os.path.join(EX, 'volumes_time.json'), encoding='utf-8'))

fig, axs = plt.subplots(2, 2, figsize=(7.09, 5.0))
fig.subplots_adjust(left=0.085, right=0.985, top=0.955, bottom=0.095, wspace=0.30, hspace=0.38)

ax = axs[0, 0]
x = prof['x'] - 130.0
for i, c in enumerate(CASES):
    ax.plot(x, prof[c], color=C[i], marker=MK[i], ms=2.2, lw=1.0, label=LAB[i])
ax.axvspan(20, 40, color='0.85', zorder=0, alpha=0.7)
ax.text(30, 78, 'diapir footprint', ha='center', va='top', fontsize=5.8, color='0.25')
ax.set_xlim(0, 70); ax.set_ylim(0, 80)
ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 70])
ax.set_xticklabels(['130', '140', '150', '160', '170', '180', '190', '200'])
ax.set_xlabel('X (km)'); ax.set_ylabel('Mean thickness in the axial corridor (m)')
ax.legend(frameon=False, fontsize=5.4, loc='upper right', handlelength=1.6, labelspacing=0.22)
panel_letter(ax, 'a', color='k', loc='left')

ax = axs[0, 1]
ax.semilogy(RDF, [m['flank_axial_ratio'] for m in M], color='#1f4e79', marker='o', ms=3.0, lw=1.1, label='Flank / axial thickness')
ax.semilogy(RDF, [m['enrichment'] for m in M], color='#b3541e', marker='s', ms=3.0, lw=1.1, label='Inside / outside diapir footprint')
ax.axhline(1.0, color='0.6', lw=0.6, ls=':')
ax.set_xlim(-0.08, 1.58); ax.set_ylim(0.08, 60); ax.set_xticks(RDF)
# plain tick text keeps every rendered glyph at or above the 5 pt floor
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: '%g' % v))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel('Rdf'); ax.set_ylabel('Thickness ratio')
ax.legend(frameon=False, fontsize=5.8, loc='upper center', handlelength=1.6)
panel_letter(ax, 'b', color='k', loc='left')

ax = axs[1, 0]
va = [V[c]['V_axial_distal'] for c in CASES]; vf = [V[c]['V_flank'] for c in CASES]
xx = np.arange(5)
ax.bar(xx - 0.19, va, 0.36, color='#1f4e79', label='Axial corridor beyond the diapir')
ax.bar(xx + 0.19, vf, 0.36, color='#b3541e', label='Diapir flanks')
for i in range(5):
    ax.text(xx[i] - 0.19, va[i] + 0.9, '%.1f' % va[i], ha='center', va='bottom', fontsize=5.0, color='#1f4e79')
    ax.text(xx[i] + 0.19, vf[i] + 0.9, '%.1f' % vf[i], ha='center', va='bottom', fontsize=5.0, color='#b3541e')
ax.set_xticks(xx); ax.set_xticklabels(SHORT); ax.set_ylim(0, 48)
ax.set_ylabel('Deposited volume at 150 kyr (km³)')
ax.legend(frameon=False, fontsize=5.8, loc='upper center', ncol=2, handlelength=1.4, columnspacing=1.0)
panel_letter(ax, 'c', color='k', loc='left')

ax = axs[1, 1]
for i, c in enumerate(CASES):
    st = VT[c]['steps']; t = np.array([s['time_kyr'] for s in st]) / 1000.0
    vl = np.array([s['V_local'] for s in st])
    ax.plot(t[1:], np.diff(vl) / 5.0 / 60.0 * 100.0, color=C[i], marker=MK[i], ms=2.2, lw=1.0, label=LAB[i])
ax.set_xlim(0, 0.155); ax.set_ylim(1.0, 2.5); ax.set_yticks([1.0, 1.5, 2.0, 2.5])
ax.set_xlabel('Time (Myr)'); ax.set_ylabel('Deposition rate (km² per 10⁵ yr)')
ax.text(0.03, 0.06, 'rate = (volume deposited per 5 kyr) / 5 kyr / 60 km', transform=ax.transAxes, fontsize=5.4, color='0.25')
panel_letter(ax, 'd', color='k', loc='left')
od = outdir('fig5')
FIG5 = os.path.join(od, 'Figure5_routing_and_mass_partitioning')
require_matplotlib_panel_alignment(
    fig, json_out=FIG5 + '.alignment.json', overlay_svg=FIG5 + '.alignment.svg',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=True)
fig.savefig(FIG5 + '.pdf')
fig.savefig(FIG5 + '.svg')
fig.savefig(FIG5 + '.png', dpi=600)
fig.savefig(FIG5 + '.tiff', dpi=600)
print('saved', FIG5, flush=True)
plt.close(fig)
print('DONE')
