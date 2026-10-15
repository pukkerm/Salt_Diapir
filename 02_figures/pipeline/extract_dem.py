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
"""Initial topographic surface for the five cases (from the base of the oldest layer)."""
import os, numpy as np, h5py
ROOT = RAW
OUT = EXTRACT
CASES = [('fan',0),('fan100',100),('fan200',200),('fan250',250),('fan300',300)]
for case, H in CASES:
    with h5py.File(os.path.join(ROOT, case, 'h5', 'sed.time1.hdf5'), 'r') as f:
        coords = np.array(f['coords'], dtype=np.float64)
        z0 = np.array(f['layElev'][:, 0], dtype=np.float32)
        z1 = np.array(f['layElev'][:, -1], dtype=np.float32)
    xi = np.unique(coords[:, 0]); yi = np.unique(coords[:, 1])
    ix = np.searchsorted(xi, coords[:, 0]); iy = np.searchsorted(yi, coords[:, 1])
    Z = np.full((yi.size, xi.size), np.nan, dtype=np.float32)
    Z[iy, ix] = z0
    np.savez_compressed(os.path.join(OUT, 'dem_%s.npz' % case), z=Z, xi=xi, yi=yi, H=np.array([H]))
    if case == 'fan':
        np.savez_compressed(os.path.join(OUT, 'dem_grid.npz'), xi=xi, yi=yi)
    print('%-8s grid %dx%d  z %.0f .. %.0f  (canyon min %.0f)' % (case, xi.size, yi.size,
          np.nanmin(Z), np.nanmax(Z), np.nanmin(Z[190:210, :])), flush=True)
print('DONE')
