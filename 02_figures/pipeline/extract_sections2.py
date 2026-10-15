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
"""Full dip-directed section (Y = 100 km, X = 130-200 km) for the five cases, timestep 30."""
import os, sys, time
import numpy as np
# stratalAnalyse (badlands_companion) reads the raw HDF5 output. It ships with
# the pyBadlands/ETL toolbox and is not part of this package; point STRATAL_DIR
# at the folder that holds stratalAnalyse.py if you rebuild the derived data.
_extra = _os.environ.get('STRATAL_DIR')
if _extra:
    sys.path.insert(0, _extra)
try:
    import stratalAnalyse as strata
except ImportError as _err:
    raise SystemExit('This script rebuilds 03_derived_data from the raw pyBadlands output and needs '
                     'stratalAnalyse (badlands_companion). Install the pyBadlands/ETL toolbox and set '
                     'STRATAL_DIR to the folder that contains stratalAnalyse.py. Missing module: %s' % _err)
ROOT = RAW
OUT  = EXTRACT
CASES = [('fan','H0',0),('fan100','H100',100),('fan200','H200',200),('fan250','H250',250),('fan300','H300',300)]
for case, label, H in CASES:
    f = os.path.join(OUT, 'sec_%s_xfull.npz' % case)
    if os.path.exists(f):
        print('skip', case, flush=True); continue
    t0 = time.time()
    cs = strata.stratalSection(folder=os.path.join(ROOT, case, 'h5'))
    cs.loadStratigraphy(timestep=30)
    cs.buildSection(xo=130000.0, yo=100000.0, xm=200000.0, ym=100000.0, pts=280, gfilter=1)
    dep = np.asarray(cs.secDep, dtype=np.float32)
    thk = np.asarray(cs.secTh, dtype=np.float32)
    dist = np.asarray(cs.dist, dtype=np.float64)
    np.savez_compressed(f, dist=dist, secDep=dep, secTh=thk, coord=np.array([100000.0]), H=np.array([H]))
    print('%s xfull nlay=%d npts=%d  base=%.1f top=%.1f thmax=%.2f  (%.0fs)' % (
        case, dep.shape[0], dep.shape[1], float(dep[0].min()), float(dep[-1].max()),
        float(np.nanmax(thk)), time.time()-t0), flush=True)
print('DONE')
