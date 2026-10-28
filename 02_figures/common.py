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
"""Shared plotting helpers for the revised manuscript figures."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl

MM = 1.0 / 25.4
EXTRACT = _os.environ.get('EXTRACT_DIR', _release_dir('*_derived_data') or _os.path.join(ROOT_DIR, '03_derived_data'))
OUTROOT = _os.environ.get('FIG_OUT', _os.path.join(_release_dir('*_figures') or ROOT_DIR, 'out'))
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
H = {'fan': 0, 'fan100': 100, 'fan200': 200, 'fan250': 250, 'fan300': 300}
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
TITLE = {'fan': '(0 m, Rdf = 0)', 'fan100': '(100 m, Rdf = 0.5)', 'fan200': '(200 m, Rdf = 1.0)',
         'fan250': '(250 m, Rdf = 1.25)', 'fan300': '(300 m, Rdf = 1.5)'}
STEPS = {10: 50, 20: 100, 30: 150}          # step index -> kyr


def set_style(base=7.0):
    mpl.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': base,
        'axes.labelsize': base,
        'axes.titlesize': base,
        'xtick.labelsize': base - 1,
        'ytick.labelsize': base - 1,
        'legend.fontsize': base - 1,
        'axes.linewidth': 0.6,
        'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
        'xtick.major.size': 2.0, 'ytick.major.size': 2.0,
        'xtick.direction': 'in', 'ytick.direction': 'in',
        'xtick.top': True, 'ytick.right': True,
        'svg.fonttype': 'none',
        'pdf.fonttype': 42, 'ps.fonttype': 42,
        'figure.facecolor': 'white', 'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
    })


def outdir(name):
    d = os.path.join(OUTROOT, name)
    os.makedirs(d, exist_ok=True)
    return d


def free_y(ax, xc, y_a, y_b, s, fontsize, pad=1.0, n=140):
    """Lowest y between y_a (deep end) and y_b where the text box crosses no drawn line.

    Scans from y_a towards y_b and keeps the box clear of axis-end ticks and the
    axes frame.  Returns None when no free band exists.
    """
    fig = ax.figure
    fig.canvas.draw()
    pts = []
    for art in list(ax.collections) + list(ax.lines) + list(ax.patches):
        if hasattr(art, 'get_array') and not hasattr(art, 'get_paths'):
            continue
        try:
            paths = art.get_paths()
        except AttributeError:
            continue
        tr = art.get_transform()
        for path in paths:
            v = tr.transform(path.vertices)
            if len(v) > 1:
                pts.append(v)
    pts = np.vstack(pts) if pts else np.zeros((0, 2))
    tmp = ax.text(xc, y_a, s, fontsize=fontsize, ha='center', va='center')
    fig.canvas.draw()
    bb = tmp.get_window_extent(fig.canvas.get_renderer())
    tmp.remove()
    w2, h2 = 0.5 * bb.width, 0.5 * bb.height
    ab = ax.get_window_extent()
    for yv in np.linspace(y_a, y_b, n):
        c = ax.transData.transform((xc, yv))
        if c[1] - h2 < ab.y0 + 4.5 or c[1] + h2 > ab.y1 - 2.0:
            continue
        if c[0] - w2 < ab.x0 + 2.0 or c[0] + w2 > ab.x1 - 2.0:
            continue
        if np.any((np.abs(pts[:, 0] - c[0]) < w2 + pad) & (np.abs(pts[:, 1] - c[1]) < h2 + pad)):
            continue
        return float(yv)
    print('WARN free_y: no free band for %r' % s, flush=True)
    return None


def save_all(fig, base, dpi=600):
    fig.savefig(base + '.png', dpi=dpi)
    fig.savefig(base + '.pdf')
    fig.savefig(base + '.svg')
    print('saved', base + '.png/.pdf/.svg', flush=True)


def panel_letter(ax, letter, color='k', size=None, loc='left', x=None, y=None):
    """Place a bold panel letter. loc: left|right|ul|ur|ll|lr."""
    pos = {'left': (0.04, 0.965), 'ul': (0.04, 0.965), 'right': (0.96, 0.965),
           'ur': (0.96, 0.965), 'll': (0.04, 0.035), 'lr': (0.96, 0.035)}.get(loc, (0.04, 0.965))
    x = pos[0] if x is None else x
    y = pos[1] if y is None else y
    ha = 'left' if x < 0.5 else 'right'
    va = 'top' if y > 0.5 else 'bottom'
    ax.text(x, y, letter, transform=ax.transAxes, fontweight='bold',
            fontsize=size or mpl.rcParams['font.size'] + 1, color=color,
            va=va, ha=ha, zorder=20)


def diapir_footprint(ax, color='w', lw=0.7, ls='--', alpha=0.95):
    from matplotlib.patches import Ellipse
    e = Ellipse((160.0, 100.0), width=20.0, height=40.0, fill=False,
                edgecolor=color, linewidth=lw, linestyle=ls, alpha=alpha, zorder=15)
    ax.add_patch(e)
    return e


def canyon_mouth(ax, color='w'):
    ax.plot([130.0], [100.0], marker='>', markersize=3.6, markerfacecolor='none',
            markeredgecolor=color, markeredgewidth=0.7, zorder=15)


def save_panel(fig, folder, name, dpi=600):
    fig.savefig(os.path.join(folder, name + '.png'), dpi=dpi)
    fig.savefig(os.path.join(folder, name + '.pdf'))
    fig.savefig(os.path.join(folder, name + '.svg'))
    plt_close(fig)


def plt_close(fig):
    import matplotlib.pyplot as _plt
    _plt.close(fig)
