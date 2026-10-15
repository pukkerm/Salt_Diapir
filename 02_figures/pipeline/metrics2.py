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
"""Additional metrics: axial longitudinal profile, volumes in km3."""
import os, json
import numpy as np
EX = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
H = {'fan': 0, 'fan100': 100, 'fan200': 200, 'fan250': 250, 'fan300': 300}
xi = np.load(os.path.join(EX, 'xi.npy')) / 1000.0
yi = np.load(os.path.join(EX, 'yi.npy')) / 1000.0
XX, YY = np.meshgrid(xi, yi)
CELL_KM2 = 0.25
AXIAL = (np.abs(YY - 100.0) <= 12.0)
edges = np.arange(130.0, 202.0, 2.0)
centres = 0.5 * (edges[:-1] + edges[1:])
prof = {}
vol = {}
for case in CASES:
    T = np.load(os.path.join(EX, 'T_step30_%s.npy' % case))
    p = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = AXIAL & (XX >= a) & (XX < b)
        p.append(float(T[m].mean()))
    prof[case] = np.array(p)
    V = lambda m: float(T[m].sum() * CELL_KM2 / 1000.0)     # m*km2 -> km3
    vol[case] = dict(
        V_local=V((XX >= 130) & (XX <= 200) & (YY >= 65) & (YY <= 135)),
        V_axial_distal=V((XX >= 168) & (XX <= 200) & (YY >= 88) & (YY <= 112)),
        V_flank=V(((XX >= 150) & (XX <= 185)) & (((YY >= 70) & (YY <= 86)) | ((YY >= 114) & (YY <= 130)))),
        V_beyond_full=V((XX >= 175) & (YY >= 0) & (YY <= 200)),
        V_beyond_axial=V((XX >= 175) & (YY >= 88) & (YY <= 112)),
        V_total=V((XX >= 0) & (YY >= 0)),
    )
np.savez(os.path.join(EX, 'axial_profiles.npz'), x=centres, **{c: prof[c] for c in CASES})
with open(os.path.join(EX, 'volumes.json'), 'w', encoding='utf-8') as fp:
    json.dump(vol, fp, indent=1)
print('%-8s %8s %8s %8s %8s %8s %8s' % ('Rdf', 'Vloc', 'Vaxdist', 'Vflank', 'VbyFull', 'VbyAx', 'Vtot'))
for c in CASES:
    v = vol[c]
    print('%-8.2f %8.1f %8.2f %8.1f %8.1f %8.2f %8.1f' % (RDF[c], v['V_local'], v['V_axial_distal'],
          v['V_flank'], v['V_beyond_full'], v['V_beyond_axial'], v['V_total']))
print()
for c in CASES:
    print('%s axial profile (2-km bins, X=131..199):' % c, np.round(prof[c], 1).tolist())
