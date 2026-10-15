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
"""Figure 4 - transverse section at X = 160 km (Y = 70-130 km, true elevation)"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, BoundaryNorm, ListedColormap, Normalize
from matplotlib.ticker import FuncFormatter, NullFormatter
from common import free_y
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import set_style, outdir, save_all, panel_letter

EX = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
ROWLAB = ['0 m  (Rdf = 0)', '100 m  (Rdf = 0.5)', '200 m  (Rdf = 1.0)', '250 m  (Rdf = 1.25)', '300 m  (Rdf = 1.5)']
BAND = 30
KIND = 'trans'
FLAT = False
DMAX = 0
set_style(7.0)
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

S = {}
for c in CASES:
    d = np.load(os.path.join(EX, 'sec_%s_%s.npz' % (c, 'y160w')))
    dep = d['secDep'].astype(float); th = np.clip(d['secTh'].astype(float), 0, None)
    dist = d['dist'] / 1000.0 + 70
    base = dep[0] - th[0]
    ifc = np.vstack([base, dep]); surf = ifc[-1]
    Z = np.minimum.accumulate(surf[None, :] - ifc, axis=0) if FLAT else ifc
    nlay = th.shape[0]
    e = np.linspace(0, nlay, nlay // BAND + 1).astype(int)
    Zb = Z[e]
    tb = np.array([th[e[b]:e[b+1]].sum(axis=0) for b in range(e.size - 1)])
    if FLAT:
        ylim = (DMAX, 0.0)
    else:
        lo = float(np.nanmin(base)); hi = float(np.nanmax(dep[-1]))
        pad = 0.05 * max(hi - lo, 250.0)
        ylim = (lo - pad, hi + pad)
    S[c] = dict(dist=dist, Z=Z, nlay=Z.shape[0] - 1, Zb=Zb, tb=tb, nb=e.size - 1, ylim=ylim)
nb = S[CASES[0]]['nb']
nlay = S[CASES[0]]['nlay']
dist = S[CASES[0]]['dist']; dx = dist[1] - dist[0]
xe = np.concatenate([[dist[0] - dx/2], (dist[:-1] + dist[1:])/2, [dist[-1] + dx/2]])
vmax_t = float(np.nanpercentile(np.concatenate([S[c]['tb'].ravel() for c in CASES]), 99.0))
cmap_full = ListedColormap(plt.get_cmap('BrBG')(np.linspace(0.08, 0.92, 300)))
cmap_lay = ListedColormap(plt.get_cmap('BrBG')(np.linspace(0.06, 0.94, nlay)))
norm_lay = BoundaryNorm(np.arange(-0.5, nlay + 0.5), nlay)
X0, X1 = 70.0, 130.0
XT = [70,85,100,115,130]
XTL = ["70","85","100","115","130"]
XLBL = 'Y (km)'
YLBL = 'Elevation (m)'
print('bands', nb, 'P99 %.2f' % vmax_t)

def draw(ax, c, which, showy):
    pc = None
    d = S[c]
    if which == 'idx':
        # one colour per stratigraphic layer: a continuous gradient, not 30 blocks
        nl = d['nlay']
        Xg = np.tile(xe, (nl + 1, 1)); Zg = np.hstack([d['Z'], d['Z'][:, -1:]])
        KI = np.tile(np.arange(nl, dtype=float)[:, None], (1, xe.size - 1))
        ax.pcolormesh(Xg, Zg, KI, cmap=cmap_lay, norm=norm_lay, shading='flat', rasterized=True)
        base = d['Z'][0]
        lines = d['Z'][::BAND]
        if lines[-1] is not d['Z'][-1]:
            lines = np.vstack([lines, d['Z'][-1]])
    else:
        Xg = np.tile(xe, (nb + 1, 1)); Zg = np.hstack([d['Zb'], d['Zb'][:, -1:]])
        pc = ax.pcolormesh(Xg, Zg, d['tb'], cmap='magma', norm=LogNorm(vmin=0.3, vmax=vmax_t),
                           shading='flat', rasterized=True)
        base = d['Zb'][0]
        lines = d['Zb']
    ax.fill_between(d['dist'], base, d['ylim'][0], color='0.88', lw=0, zorder=0)
    for k in range(lines.shape[0]):
        ax.plot(d['dist'], lines[k], color='k', lw=0.35 if (k % 5 == 0) else 0.15, alpha=0.85, zorder=4)
    ax.set_xlim(X0, X1); ax.set_ylim(d['ylim'][0], d['ylim'][1])
    ax.set_xticks(XT); ax.set_xticklabels(XTL)
    ax.tick_params(labelsize=6.2)
    ax.set_xlabel(XLBL, labelpad=1.5)
    if showy:
        ax.set_ylabel(YLBL)
    if which != 'idx':
        return pc
    sp = d['ylim'][1] - d['ylim'][0]
    xref = X0 + 0.5 * (X1 - X0)
    ytop = d['ylim'][1] - 0.01 * sp
    ax.annotate('', xy=(xref, d['ylim'][1] - 0.11 * sp), xytext=(xref, ytop),
                arrowprops=dict(arrowstyle='-|>', color='#c00000', lw=2.0), zorder=8)
    # the label sits in the blank basement and is tied to the structure by a leader
    ylab = free_y(ax, xref, d['ylim'][0] + 0.02 * sp, d['ylim'][0] + 0.35 * sp, 'diapir', 5.8)
    if ylab is None:
        ylab = d['ylim'][0] + 0.05 * sp
    ax.annotate('diapir', xy=(xref, ytop), xytext=(xref, ylab),
                fontsize=5.8, color='#c00000', ha='center', va='center', zorder=8,
                arrowprops=dict(arrowstyle='-', color='#c00000', lw=0.5,
                                linestyle=(0, (2, 2)), shrinkA=9, shrinkB=1))
    return pc

fig = plt.figure(figsize=(7.09, 8.15))
gs = fig.add_gridspec(6, 3, width_ratios=[0.17, 1, 1], height_ratios=[1, 1, 1, 1, 1, 0.12],
                      wspace=0.08, hspace=0.50, left=0.055, right=0.985, top=0.945, bottom=0.085)
axs = []; pc = None; EXCL = []
for i, c in enumerate(CASES):
    ax = fig.add_subplot(gs[i, 1]); axs.append(ax)
    draw(ax, c, 'idx', i == 0)
    ax.set_xticklabels([] if i < len(CASES) - 1 else XTL)
    ax.text(0.0, 1.008, 'acegi'[i], transform=ax.transAxes, fontsize=8.0, fontweight='bold',
            ha='left', va='bottom', clip_on=False, zorder=20)
    if i == 0:
        ax.set_title('Chronostratigraphic framework', fontsize=6.8, pad=4)
    axl = fig.add_subplot(gs[i, 0]); axl.axis('off'); EXCL.append(axl)
    axl.text(0.35, 0.5, ROWLAB[i], rotation=90, rotation_mode='anchor', ha='center', va='center', fontsize=6.5)
    ax2 = fig.add_subplot(gs[i, 2])
    pc = draw(ax2, c, 'thick', False)
    ax2.set_yticklabels([])
    ax2.set_xticklabels([] if i < len(CASES) - 1 else XTL)
    ax2.text(0.0, 1.008, 'bdfhj'[i], transform=ax2.transAxes, fontsize=8.0, fontweight='bold',
             ha='left', va='bottom', clip_on=False, zorder=20)
    if i == 0:
        ax2.set_title('Band thickness (5 kyr)', fontsize=6.8, pad=4)
cax = fig.add_subplot(gs[5, 1])
cb = fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(0, nlay - 1), cmap=cmap_lay), cax=cax, orientation='horizontal')
cb.set_label('Layer index (0 = oldest, %d = youngest; one colour per 0.5 kyr layer)' % (nlay - 1), fontsize=6.3)
cb.ax.tick_params(labelsize=6.0); cb.set_ticks([0, 60, 120, 180, 240, 300]); EXCL.append(cb.ax)
cax2 = fig.add_subplot(gs[5, 2])
cb2 = fig.colorbar(pc, cax=cax2, orientation='horizontal')
cb2.set_label('Thickness per 5-kyr band (m)', fontsize=6.4); cb2.ax.tick_params(labelsize=6.0); EXCL.append(cb2.ax)
# plain tick text keeps every rendered glyph at or above the 5 pt floor
cb2.ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: '%g' % v))
cb2.ax.xaxis.set_minor_formatter(NullFormatter())
fig.text(0.012, 0.50, YLBL, rotation=90, rotation_mode='anchor', ha='center', va='center', fontsize=6.6)
od = outdir('fig4')
FIG4 = os.path.join(od, 'Figure4_transverse_section')
require_matplotlib_panel_alignment(
    fig, json_out=FIG4 + '.alignment.json', overlay_svg=FIG4 + '.alignment.svg',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5, require_panel_labels=True, exclude_axes=EXCL)
fig.savefig(FIG4 + '.pdf', dpi=600)
fig.savefig(FIG4 + '.svg', dpi=600)
fig.savefig(FIG4 + '.png', dpi=600)
fig.savefig(FIG4 + '.tiff', dpi=600)
print('saved', FIG4, flush=True)
fig.canvas.draw()
e0 = axs[0].get_window_extent(); dpi = fig.dpi
pw = e0.width / dpi * 25.4; phh = e0.height / dpi * 25.4
for c in CASES:
    zr = S[c]['ylim'][1] - S[c]['ylim'][0]
    print(c, 'panel %.1f x %.1f mm  VE %.0fx' % (pw, phh, ((X1 - X0) * 1000.0 / pw) / (zr / phh)))
plt.close(fig)

pd = os.path.join(od, 'panels'); os.makedirs(pd, exist_ok=True)
for i, c in enumerate(CASES):
    for which, nm in [('idx', 'layerindex'), ('thick', 'bandthickness')]:
        f = plt.figure(figsize=(3.8, 1.6))
        a = f.add_axes([0.16, 0.235, 0.81, 0.70])
        draw(a, c, which, True)
        a.text(0.015, 0.95, ROWLAB[i], transform=a.transAxes, fontsize=6.5, va='top')
        f.savefig(os.path.join(pd, 'panel_%s_%s.png' % (c, nm)), dpi=600)
        f.savefig(os.path.join(pd, 'panel_%s_%s.svg' % (c, nm)))
        plt.close(f)
f = plt.figure(figsize=(3.6, 0.5)); a = f.add_axes([0.05, 0.55, 0.90, 0.35])
cb = f.colorbar(plt.cm.ScalarMappable(norm=Normalize(0, nlay - 1), cmap=cmap_lay), cax=a, orientation='horizontal')
cb.set_label('Layer index', fontsize=6.5); cb.ax.tick_params(labelsize=6.0)
f.savefig(os.path.join(pd, 'colorbar_layerindex.png'), dpi=600); f.savefig(os.path.join(pd, 'colorbar_layerindex.svg')); plt.close(f)
f = plt.figure(figsize=(3.6, 0.5)); a = f.add_axes([0.05, 0.55, 0.90, 0.35])
cb = f.colorbar(plt.cm.ScalarMappable(norm=LogNorm(vmin=0.3, vmax=vmax_t), cmap='magma'), cax=a, orientation='horizontal')
cb.set_label('Thickness per 5-kyr band (m)', fontsize=6.5); cb.ax.tick_params(labelsize=6.0)
f.savefig(os.path.join(pd, 'colorbar_bandthickness.png'), dpi=600); f.savefig(os.path.join(pd, 'colorbar_bandthickness.svg')); plt.close(f)
print('DONE')
