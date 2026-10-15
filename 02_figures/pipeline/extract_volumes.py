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
"""Cumulative preserved deposition volume through time for the five cases."""
import os, sys, json, time
import numpy as np
import h5py
ROOT = RAW
OUT  = EXTRACT
CASES = ['fan','fan100','fan200','fan250','fan300']
AREA = 0.25  # km2 per cell (500 m grid)
CHUNK = 20000
res = {}
for case in CASES:
    h5f = os.path.join(ROOT, case, 'h5')
    with h5py.File(os.path.join(h5f, 'sed.time30.hdf5'), 'r') as f:
        coords = np.array(f['coords'], dtype=np.float64)
    x = coords[:, 0]; y = coords[:, 1]
    m_local = (x >= 0) & (x <= 250000) & (y >= 70000) & (y <= 130000)
    m_ax = (x >= 168000) & (x <= 200000) & (y >= 88000) & (y <= 112000)
    m_fl = (x >= 150000) & (x <= 185000) & (((y >= 70000) & (y <= 86000)) | ((y >= 114000) & (y <= 130000)))
    m_by = (x >= 175000)
    n = x.shape[0]
    steps = []
    for ts in range(1, 31):
        p = os.path.join(h5f, 'sed.time%d.hdf5' % ts)
        if not os.path.exists(p):
            print('missing', case, ts, flush=True); continue
        t0 = time.time()
        with h5py.File(p, 'r') as f:
            shp = f['layThick'].shape
            tot = np.zeros(shp[0], dtype=np.float64)
            for i in range(0, shp[0], CHUNK):
                tot[i:i+CHUNK] = np.asarray(f['layThick'][i:i+CHUNK, :], dtype=np.float64).sum(axis=1)
        rec = dict(step=ts, time_kyr=ts*5.0,
                   V_local=float(tot[m_local].sum())*AREA/1000.0,
                   V_total=float(tot.sum())*AREA/1000.0,
                   V_axial=float(tot[m_ax].sum())*AREA/1000.0,
                   V_flank=float(tot[m_fl].sum())*AREA/1000.0,
                   V_beyond=float(tot[m_by].sum())*AREA/1000.0,
                   mean_thick_local=float(tot[m_local].mean()))
        steps.append(rec)
        print('%s step%02d %.1f kyr  Vloc=%.1f km3  Vtot=%.1f  Vax=%.2f  Vfl=%.1f  (%.0fs)' % (
            case, ts, ts*5.0, rec['V_local'], rec['V_total'], rec['V_axial'], rec['V_flank'], time.time()-t0), flush=True)
    res[case] = dict(cells_local=int(m_local.sum()), cells_ax=int(m_ax.sum()), cells_flank=int(m_fl.sum()), steps=steps)
with open(os.path.join(OUT, 'volumes_time.json'), 'w', encoding='utf-8') as fp:
    json.dump(res, fp, indent=1)
print('DONE')
