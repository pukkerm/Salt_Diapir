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
"""Extract stratal sections and thickness maps for the diapir routing experiment."""
import os, sys, time, json
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
SECTIONS = [
    ('x100',  'x', 100000.0, (140000.0,100000.0), (160000.0,100000.0)),   # dip-parallel, Y = 100 km
    ('y150',  'y', 150000.0, (150000.0, 80000.0), (150000.0,120000.0)),   # dip-transverse, stoss edge
    ('y160',  'y', 160000.0, (160000.0, 80000.0), (160000.0,120000.0)),   # dip-transverse, crest
    ('y170',  'y', 170000.0, (170000.0, 80000.0), (170000.0,120000.0)),   # dip-transverse, lee edge
]
TS = 30
PTS = 200
meta = {}

for case, label, H in CASES:
    if os.path.exists(os.path.join(OUT, 'thick_%s.npy' % case)) and os.path.exists(os.path.join(OUT, 'sec_%s_y170.npz' % case)):
        print('%s already extracted, skip' % case, flush=True)
        continue
    folder = os.path.join(ROOT, case, 'h5')
    t0 = time.time()
    cs = strata.stratalSection(folder=folder)
    cs.loadStratigraphy(timestep=TS)
    nz = cs.nz
    th = np.asarray(cs.th, dtype=np.float32)      # (ny, nx, nz)
    print('%s: nx=%d ny=%d nz=%d loaded %.1fs' % (case, cs.nx, cs.ny, nz, time.time()-t0), flush=True)

    # ---- total sediment thickness map ----
    T = th.sum(axis=2)                            # (ny, nx)
    np.save(os.path.join(OUT, 'thick_%s.npy' % case), T)
    xi = np.asarray(cs.xi, dtype=np.float64)
    yi = np.asarray(cs.yi, dtype=np.float64)
    np.save(os.path.join(OUT, 'xi.npy'), xi)
    np.save(os.path.join(OUT, 'yi.npy'), yi)

    # ---- sections ----
    sec_info = {}
    for sid, direction, coord, (xo, yo), (xm, ym) in SECTIONS:
        cs.buildSection(xo=xo, yo=yo, xm=xm, ym=ym, pts=PTS, gfilter=1)
        dep = np.asarray(cs.secDep, dtype=np.float32)
        thk = np.asarray(cs.secTh, dtype=np.float32)
        dist = np.asarray(cs.dist, dtype=np.float64)
        np.savez_compressed(os.path.join(OUT, 'sec_%s_%s.npz' % (case, sid)),
                            dist=dist, secDep=dep, secTh=thk, coord=np.array([coord]), H=np.array([H]))
        sec_info[sid] = dict(coord=coord, nlay=int(dep.shape[0]),
                             top_min=float(np.nanmin(dep[-1])), top_max=float(np.nanmax(dep[-1])),
                             th_max=float(np.nanmax(thk)), th_sum=float(np.nansum(thk)))
        print('   %-5s dist %.0f-%.0f m  nlay=%d  top elev %.1f..%.1f  thmax=%.2f' %
              (sid, dist[0], dist[-1], dep.shape[0], sec_info[sid]['top_min'], sec_info[sid]['top_max'], sec_info[sid]['th_max']), flush=True)

    del th, T
    meta[case] = dict(label=label, H=H, Rdf=H/200.0, nz=int(nz), nx=int(cs.nx), ny=int(cs.ny), sections=sec_info)
    print('   done %s in %.1f s\n' % (case, time.time()-t0), flush=True)

with open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=1)
print('ALL DONE')
