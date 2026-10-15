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
"""Band-thickness statistics for every 5 kyr band, plus the deposition-rate windows."""
import json, os
import h5py
import numpy as np

ROOT = RAW
OUT = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
AREA = 0.25
CHUNK = 4000
NB = 30

out = {}
for case in CASES:
    p = os.path.join(ROOT, case, 'h5', 'sed.time30.hdf5')
    with h5py.File(p, 'r') as f:
        coords = np.asarray(f['coords'], dtype=np.float64)
        x = coords[:, 0] / 1000.0; y = coords[:, 1] / 1000.0
        n = x.shape[0]
        bs = np.zeros((n, NB))
        for i in range(0, n, CHUNK):
            j = min(i + CHUNK, n)
            a = np.asarray(f['layThick'][i:j, :], dtype=np.float64)
            for b in range(NB):
                bs[i:j, b] = a[:, b * 10:(b + 1) * 10].sum(axis=1)
    m_prox = (x >= 130) & (x <= 160) & (np.abs(y - 100) <= 20)
    m_flank = (x >= 150) & (x <= 185) & (np.abs(y - 100) >= 14) & (np.abs(y - 100) <= 30)
    m_crest = (x >= 157) & (x <= 163) & (np.abs(y - 100) <= 10)
    m_axial = (x >= 168) & (x <= 200) & (np.abs(y - 100) <= 12)
    m_wing = (x >= 130) & (x <= 150) & (np.abs(y - 100) >= 20) & (np.abs(y - 100) <= 40)
    m_foot = ((x - 160.0) / 10.0) ** 2 + ((y - 100.0) / 20.0) ** 2 <= 1.0
    r = dict(case=case, Rdf=RDF[case],
             band_global_max=float(bs.max()),
             band_global_max_at=int(np.unravel_index(bs.argmax(), bs.shape)[1]),
             band_prox_max=float(bs[m_prox].max()),
             band_prox_max_at=int(np.argmax(bs[m_prox].max(axis=0))),
             band_flank_max=float(bs[m_flank].max()),
             band_crest_mean_last=float(bs[m_crest, -1].mean()),
             band_crest_max=float(bs[m_crest].max()),
             band_axial_mean_last=float(bs[m_axial, -1].mean()),
             band_wing_mean_last=float(bs[m_wing, -1].mean()),
             band_foot_mean_last=float(bs[m_foot, -1].mean()),
             band_last_global_max=float(bs[:, -1].max()),
             band_series_prox_max=[round(float(v), 2) for v in bs[m_prox].max(axis=0)])
    out[case] = r
    print('%-7s band_max=%.2f (band %d)  prox_max=%.2f (band %d)  flank_max=%.2f  last_crest=%.2f  last_axial=%.2f  last_wing=%.2f' % (
        case, r['band_global_max'], r['band_global_max_at'] + 1, r['band_prox_max'], r['band_prox_max_at'] + 1,
        r['band_flank_max'], r['band_crest_mean_last'], r['band_axial_mean_last'], r['band_wing_mean_last']), flush=True)
    print('    prox band maxima: ' + ' '.join('%.1f' % v for v in r['band_series_prox_max']), flush=True)

with open(os.path.join(OUT, 'bands_fig5.json'), 'w', encoding='utf-8') as fp:
    json.dump(out, fp, indent=1)

# ---- deposition-rate windows from the time series already extracted
VT = json.load(open(os.path.join(OUT, 'volumes_time.json'), encoding='utf-8'))
print('\n=== deposition rate, mean over 0-50 / 50-100 / 100-150 kyr (10^-5 km2/yr) ===')
rate = {}
for case in CASES:
    st = sorted(VT[case]['steps'], key=lambda s: s['time_kyr'])
    t = np.array([s['time_kyr'] for s in st]); v = np.array([s['V_local'] for s in st])
    dt = np.diff(t); r = np.diff(v) / dt / 60.0 * 100.0
    mid = 0.5 * (t[:-1] + t[1:])
    win = {}
    for lo, hi in ((0, 50), (50, 100), (100, 150)):
        m = (mid >= lo) & (mid < hi)
        win['%d_%d' % (lo, hi)] = float(r[m].mean())
    win['all'] = float(r.mean())
    rate[case] = win
    print('%-7s  %.2f  %.2f  %.2f   (whole run %.2f)' % (case, win['0_50'], win['50_100'], win['100_150'], win['all']))
with open(os.path.join(OUT, 'rates_fig5.json'), 'w', encoding='utf-8') as fp:
    json.dump(rate, fp, indent=1)
print('\nwrote bands_fig5.json and rates_fig5.json')
