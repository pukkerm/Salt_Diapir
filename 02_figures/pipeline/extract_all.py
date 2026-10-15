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
"""All-timestep cumulative sediment thickness maps (Steps 0-30) for every case."""
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
CASES = ['fan','fan100','fan200','fan250','fan300']
for case in CASES:
    for ts in range(0, 31):
        f = os.path.join(OUT, 'T_step%02d_%s.npy' % (ts, case))
        if os.path.exists(f):
            continue
        t0 = time.time()
        cs = strata.stratalSection(folder=os.path.join(ROOT, case, 'h5'))
        cs.loadStratigraphy(timestep=ts)
        T = np.asarray(cs.th, dtype=np.float32).sum(axis=2)
        np.save(f, T)
        print('%s step%02d  Tmax=%.2f  Tmean=%.3f  (%.0fs)' % (case, ts, np.nanmax(T), np.nanmean(T), time.time()-t0), flush=True)
        del T
print('DONE')
