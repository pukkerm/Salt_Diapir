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
"""Per-stage statistics (50/100/150 kyr) on the cumulative-thickness maps."""
import json, os
import numpy as np
EX = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
xi = np.load(os.path.join(EX, 'xi.npy')) / 1000.0
yi = np.load(os.path.join(EX, 'yi.npy')) / 1000.0
XX, YY = np.meshgrid(xi, yi)
M = {
 'proximal': (XX >= 130) & (XX <= 160) & (np.abs(YY - 100) <= 20),
 'front':    (XX >= 150) & (XX <= 162) & (np.abs(YY - 100) <= 15),
 'crest':    (XX >= 157) & (XX <= 163) & (np.abs(YY - 100) <= 10),
 'axial':    (XX >= 168) & (XX <= 200) & (np.abs(YY - 100) <= 12),
 'lee40':    (XX >= 195) & (XX <= 205) & (np.abs(YY - 100) <= 12),
 'flank':    (XX >= 150) & (XX <= 185) & (np.abs(YY - 100) >= 14) & (np.abs(YY - 100) <= 30),
 'wing':     (XX >= 130) & (XX <= 150) & (np.abs(YY - 100) >= 20) & (np.abs(YY - 100) <= 40),
 'foot':     ((XX - 160.0) / 10.0) ** 2 + ((YY - 100.0) / 20.0) ** 2 <= 1.0,
}
out = {}
for case in CASES:
    r = dict(case=case, Rdf=RDF[case])
    for ts, ky in ((10, 50), (20, 100), (30, 150)):
        f = os.path.join(EX, 'T_step%02d_%s.npy' % (ts, case))
        T = np.load(f)
        for k, mk in M.items():
            if mk.shape != T.shape: mk = mk.T
            r['%s_%d_mean' % (k, ky)] = float(np.nanmean(T[mk]))
            r['%s_%d_max' % (k, ky)] = float(np.nanmax(T[mk]))
    out[case] = r
with open(os.path.join(EX, 'stages_fig5.json'), 'w', encoding='utf-8') as fp:
    json.dump(out, fp, indent=1)
hdr = ['proximal','front','crest','axial','lee40','flank','wing','foot']
print('case     stage  ' + ''.join(h.rjust(10) for h in hdr) + '   (mean cumulative thickness, m)')
for case in CASES:
    r = out[case]
    for ky in (50, 100, 150):
        print('%-8s %4d  ' % (case, ky) + ''.join(('%.2f' % r['%s_%d_mean' % (h, ky)]).rjust(10) for h in hdr))
    print('         max150  ' + ''.join(('%.1f' % r['%s_150_max' % h]).rjust(10) for h in hdr))
