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
"""Figure 1 - model setup: initial topography, canyon geometry and diapir geometry.

Publication QA: the source carries the explicit font, editable-text and export
settings required by nature-figure, and the render-time panel-alignment gate.
Physiographic labels are placed by clear_pos(), which searches for the nearest
position whose rendered text box is crossed by no drawn line (contours, section
line, canyon/diapir outlines).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import set_style, outdir
try:
    from audit_panel_alignment import require_matplotlib_panel_alignment
except Exception:  # optional layout audit; not required to reproduce the figure
    def require_matplotlib_panel_alignment(*args, **kwargs):
        return None

EX = EXTRACT
CASES = [('fan', 0), ('fan100', 100), ('fan200', 200), ('fan250', 250), ('fan300', 300)]
LAB = ['0 m (Rdf = 0)', '100 m (Rdf = 0.5)', '200 m (Rdf = 1.0)', '250 m (Rdf = 1.25)', '300 m (Rdf = 1.5)']
COL = ['#1f4e79', '#2e75b6', '#7f7f7f', '#bf9000', '#d9d200']
set_style(7.0)
# --- explicit publication settings (audited by nature-figure validate_figure.py) ---
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'Liberation Sans', 'DejaVu Sans']
mpl.rcParams.update({
    'svg.fonttype': 'none',
    'pdf.fonttype': 42,
})

g = np.load(os.path.join(EX, 'dem_grid.npz'))
xi = g['xi'] / 1000.0; yi = g['yi'] / 1000.0
Z = {c: np.load(os.path.join(EX, 'dem_%s.npz' % c))['z'] for c, _ in CASES}
j = int(np.argmin(np.abs(yi - 100.0)))

fig = plt.figure(figsize=(7.09, 3.4))
axa = fig.add_axes([0.055, 0.185, 0.375, 0.66])
axb = fig.add_axes([0.545, 0.615, 0.385, 0.30])
axc = fig.add_axes([0.545, 0.185, 0.385, 0.30])

im = axa.imshow(Z['fan250'], origin='lower', extent=(xi[0], xi[-1], yi[0], yi[-1]),
                cmap='terrain', vmin=-3500, vmax=2500, interpolation='nearest')
axa.contour(xi, yi, Z['fan250'], levels=[-3000, -2000, -1000, 0, 1000, 2000], colors='k', linewidths=0.25, alpha=0.6)
axa.add_patch(Ellipse((160, 100), 20, 40, fill=False, ec='w', lw=0.8, ls=(0, (4, 2)), zorder=6))
axa.add_patch(Ellipse((130, 100), 30, 8, fill=False, ec='w', lw=0.8, ls=(0, (1, 1.4)), zorder=6))
axa.plot([0, 250], [100, 100], color='w', lw=0.6, ls=(0, (5, 3)), zorder=5)
axa.set_xlim(0, 250); axa.set_ylim(0, 200)
axa.set_xticks([0, 50, 100, 150, 200, 250]); axa.set_yticks([0, 50, 100, 150, 200])
axa.tick_params(labelsize=6.0); axa.set_xlabel('X (km)'); axa.set_ylabel('Y (km)')
axa.set_title('Initial topography (250 x 200 km, 500 m grid)', fontsize=6.6, pad=3)

# ---------------- collision-free label placement ----------------
_OBS = []          # display-space boxes already occupied by labels


def _obstacles(ax):
    """Every drawn line/patch/mesh outline in the axes, densified to <=4 pt steps."""
    fig.canvas.draw()
    out = []
    for art in list(ax.collections) + list(ax.lines) + list(ax.patches):
        try:
            paths = art.get_paths()
        except AttributeError:
            continue
        for path in paths:
            v = art.get_transform().transform(path.vertices)
            if len(v) < 2:
                continue
            step = np.hypot(np.diff(v[:, 0]), np.diff(v[:, 1]))
            if step.max() > 4.0:
                dense = [v[-1:]]
                for k in range(len(v) - 1):
                    n = max(2, int(np.ceil(step[k] / 4.0)) + 1)
                    f = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
                    dense.append(v[k][None, :] + f * (v[k + 1] - v[k])[None, :])
                v = np.vstack(dense)
            out.append(v)
    return np.vstack(out) if out else np.zeros((0, 2))


def clear_pos(ax, x, y, s, fontsize, max_r=26.0, step=1.5, pad=1.0, color='w', **kw):
    """Nearest (x, y) in data coords whose rendered box no drawn line crosses."""
    pts = _obstacles(ax)
    ab = ax.get_window_extent()
    tmp = ax.text(x, y, s, fontsize=fontsize, color=color, **kw)
    fig.canvas.draw()
    bb = tmp.get_window_extent(fig.canvas.get_renderer())
    w2, h2 = 0.5 * bb.width, 0.5 * bb.height
    cx, cy = ax.transData.transform((x, y))
    # the anchor is not the box centre for ha='left'/va='top' etc.
    ox = 0.5 * (bb.x0 + bb.x1) - cx
    oy = 0.5 * (bb.y0 + bb.y1) - cy
    best, found = (cx, cy), False
    for rad in np.arange(0.0, max_r + 1e-9, step):
        n = 1 if rad == 0 else max(16, int(2 * np.pi * rad / step))
        for a in np.linspace(0.0, 2 * np.pi, n, endpoint=False):
            px, py = cx + rad * np.cos(a), cy + rad * np.sin(a)
            bx, by = px + ox, py + oy
            if (bx - w2 < ab.x0 + 2.0 or bx + w2 > ab.x1 - 2.0
                    or by - h2 < ab.y0 + 2.0 or by + h2 > ab.y1 - 2.0):
                continue
            if np.any((np.abs(pts[:, 0] - bx) < w2 + pad) & (np.abs(pts[:, 1] - by) < h2 + pad)):
                continue
            clash = False
            for o in _OBS:
                if abs(bx - o[0]) < w2 + o[2] + 2 and abs(by - o[1]) < h2 + o[3] + 2:
                    clash = True
                    break
            if clash:
                continue
            best, found = (px, py), True
            break
        if found:
            break
    if not found:
        print('WARN clear_pos: no free spot for %r' % s, flush=True)
    tmp.remove()
    _OBS.append((best[0] + ox, best[1] + oy, w2, h2))
    return tuple(ax.transData.inverted().transform(best)) + (w2, h2)


TXT_KW = dict(ha='center', va='center')
for tx, ty, txt in [(25, 168, 'source area'), (75, 118, 'alluvial plain'), (112, 62, 'outer shelf'),
                    (152, 40, 'slope'), (215, 150, 'deep basin')]:
    lx, ly = clear_pos(axa, tx, ty, txt, 6.0, max_r=34.0, **TXT_KW)[:2]
    axa.text(lx, ly, txt, color='w', fontsize=6.0, zorder=7, **TXT_KW)

for tgt, nom, txt in [((130, 103), (96, 74), 'canyon'), ((160, 118), (176, 136), 'diapir')]:
    lx, ly, w2, h2 = clear_pos(axa, nom[0], nom[1], txt, 6.0, max_r=16.0, **TXT_KW)
    t0 = np.array(axa.transData.transform((lx, ly)))
    d = np.array(axa.transData.transform(tgt)) - t0
    d = d / (np.hypot(d[0], d[1]) + 1e-9)
    k = min(abs(w2 / d[0]) if abs(d[0]) > 1e-6 else 1e9,
            abs(h2 / d[1]) if abs(d[1]) > 1e-6 else 1e9) + 2.0
    p0 = tuple(axa.transData.inverted().transform(t0 + d * k))
    axa.annotate('', xy=tgt, xytext=p0, zorder=7,
                 arrowprops=dict(arrowstyle='-', color='w', lw=0.5, shrinkA=0, shrinkB=1))
    axa.text(lx, ly, txt, color='w', fontsize=6.0, zorder=8, **TXT_KW)

# panel letters sit just outside the top-left corner: no drawn line can cross them
for a, lab in ((axa, 'a'), (axb, 'b'), (axc, 'c')):
    a.text(0.0, 1.008, lab, transform=a.transAxes, fontsize=8.0, fontweight='bold',
           ha='left', va='bottom', clip_on=False, zorder=20)

cax = fig.add_axes([0.055, 0.075, 0.375, 0.035])
cb = fig.colorbar(im, cax=cax, orientation='horizontal')
cb.set_label('Elevation (m)', fontsize=6.2); cb.ax.tick_params(labelsize=5.8)

j2 = int(np.argmin(np.abs(yi - 112.0)))
axb.plot(xi, Z['fan250'][j2, :], color='0.45', lw=0.7, ls=(0, (4, 2)))
axb.fill_between(xi, Z['fan250'][j, :], -1400, color='0.88', lw=0)
axb.plot(xi, Z['fan250'][j, :], color='k', lw=0.9)
axb.set_xlim(110, 150); axb.set_ylim(-1000, -50)
axb.set_xticks([110, 120, 130, 140, 150]); axb.set_yticks([-900, -600, -300])
axb.tick_params(labelsize=6.0); axb.set_xlabel('X (km)'); axb.set_ylabel('Elevation (m)')
axb.set_title('Canyon geometry', fontsize=6.4, pad=3)
a1 = float(Z['fan250'][j, np.argmin(np.abs(xi - 127.5))]); a2 = float(Z['fan250'][j2, np.argmin(np.abs(xi - 127.5))])
axb.annotate('', xy=(127.5, a1), xytext=(127.5, a2), arrowprops=dict(arrowstyle='<->', color='#c00000', lw=0.8))
axb.annotate('canyon depth 200 m', xy=(127.5, 0.5 * (a1 + a2)), xytext=(113.5, -700), fontsize=5.4, color='#c00000',
             va='center', ha='left', arrowprops=dict(arrowstyle='-', color='#c00000', lw=0.5, shrinkA=1, shrinkB=2))
axb.annotate('', xy=(115, -930), xytext=(145, -930), arrowprops=dict(arrowstyle='<->', color='#c00000', lw=0.7))
axb.text(130, -895, 'canyon length 30 km', fontsize=5.4, color='#c00000', ha='center')
axb.text(110.5, -830, 'dashed: profile outside the canyon (Y = 112 km)', fontsize=5.0, color='0.35')

for (c, H), lab, col in zip(CASES, LAB, COL):
    axc.plot(xi, Z[c][j, :], color=col, lw=0.9, label=lab)
axc.set_xlim(146, 182); axc.set_ylim(-1180, -420)
axc.set_xticks([150, 160, 170, 180]); axc.set_yticks([-1100, -900, -700, -500])
axc.tick_params(labelsize=6.0); axc.set_xlabel('X (km)'); axc.set_ylabel('Elevation (m)')
axc.set_title('Diapir geometry (five reliefs)', fontsize=6.4, pad=3)
axc.legend(fontsize=5.2, ncol=1, loc='upper right', handlelength=1.3, columnspacing=0.8, labelspacing=0.25, framealpha=0.95, borderpad=0.3)
axc.annotate('', xy=(152, float(Z['fan'][j, np.argmin(np.abs(xi - 152))])), xytext=(152, float(Z['fan300'][j, np.argmin(np.abs(xi - 152))])),
             arrowprops=dict(arrowstyle='<->', color='#c00000', lw=0.8))
axc.text(146.6, -1080, 'diapir relief 0-300 m', fontsize=5.4, color='#c00000', ha='left', va='center')

od = outdir('fig1')
FIG1 = os.path.join(od, 'Figure1_model_setup')
require_matplotlib_panel_alignment(
    fig,
    json_out=FIG1 + '.alignment.json',
    overlay_svg=FIG1 + '.alignment.svg',
    tolerance_pt=1.5, gutter_tolerance_pt=1.5,
    require_panel_labels=True,
    panel_ids={axa: 'a', axb: 'b', axc: 'c'},
    column_groups=[['b', 'c']],
    exclude_axes=[cax, cb.ax],
)
fig.savefig(FIG1 + '.pdf')
fig.savefig(FIG1 + '.svg')
fig.savefig(FIG1 + '.png', dpi=600)
fig.savefig(FIG1 + '.tiff', dpi=600)
print('saved', FIG1, flush=True)
plt.close(fig)
print('DONE')
