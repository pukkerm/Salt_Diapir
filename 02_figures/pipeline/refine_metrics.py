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
"""Recompute the numbers quoted in the results text with the same windows as Fig. 5.

Reads the raw Badlands output (sed.time30.hdf5) so the reported quantities and the
plotted quantities share one definition.
"""
import json, os
import h5py
import numpy as np

ROOT = RAW
OUT = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
AREA = 0.25          # km2 per cell (500 m grid)
CHUNK = 4000

res = {}
for case in CASES:
    p = os.path.join(ROOT, case, 'h5', 'sed.time30.hdf5')
    with h5py.File(p, 'r') as f:
        coords = np.asarray(f['coords'], dtype=np.float64)
        x = coords[:, 0] / 1000.0
        y = coords[:, 1] / 1000.0
        shp = f['layThick'].shape
        n, nlay = shp
        tot = np.zeros(n); band = np.zeros(n)
        for i in range(0, n, CHUNK):
            j = min(i + CHUNK, n)
            a = np.asarray(f['layThick'][i:j, :], dtype=np.float64)
            tot[i:j] = a.sum(axis=1)
            band[i:j] = a[:, -10:].sum(axis=1)
    m_foot = ((x - 160.0) / 10.0) ** 2 + ((y - 100.0) / 20.0) ** 2 <= 1.0
    m_axial = (x >= 168) & (x <= 200) & (np.abs(y - 100) <= 12)
    m_flank = (x >= 150) & (x <= 185) & (np.abs(y - 100) >= 14) & (np.abs(y - 100) <= 30)
    m_crest = (x >= 157) & (x <= 163) & (np.abs(y - 100) <= 10)
    m_lee40 = (x >= 195) & (x <= 205) & (np.abs(y - 100) <= 12)
    m_wing = (x >= 130) & (x <= 150) & (np.abs(y - 100) >= 20) & (np.abs(y - 100) <= 40)
    m_prox = (x >= 130) & (x <= 160) & (np.abs(y - 100) <= 20)
    m_local = (x >= 130) & (x <= 200) & (y >= 65) & (y <= 135)
    r = dict(case=case, Rdf=RDF[case], nlay=int(nlay),
             cells=dict(foot=int(m_foot.sum()), axial=int(m_axial.sum()), flank=int(m_flank.sum()),
                        crest=int(m_crest.sum()), lee40=int(m_lee40.sum()), wing=int(m_wing.sum())))
    for nm, mk in (('footprint', m_foot), ('axial', m_axial), ('flank', m_flank),
                   ('crest', m_crest), ('lee40', m_lee40), ('wing', m_wing), ('proximal', m_prox)):
        r['T_' + nm + '_mean'] = float(tot[mk].mean())
        r['T_' + nm + '_max'] = float(tot[mk].max())
        r['B_' + nm + '_mean'] = float(band[mk].mean())
        r['B_' + nm + '_max'] = float(band[mk].max())
        r['B_' + nm + '_p95'] = float(np.percentile(band[mk], 95))
    r['T_global_max'] = float(tot.max())
    r['B_global_max'] = float(band.max())
    r['V_local_km3'] = float(tot[m_local].sum() * AREA / 1000.0)
    res[case] = r
    print('%s nlay=%d  band_max=%.2f m  T_local_mean=%.2f  T_foot=%.2f' % (
        case, nlay, r['B_global_max'], float(tot[m_local].mean()), r['T_footprint_mean']), flush=True)

# cross-check against the section-based cumulative thickness already cached
import glob
print('\ncheck tot vs T_step30:')
for case in CASES:
    f = os.path.join(OUT, 'T_step30_%s.npy' % case)
    if os.path.exists(f):
        T = np.load(f)
        print('  %-7s cached max=%.2f mean=%.4f' % (case, np.nanmax(T), np.nanmean(T)))

with open(os.path.join(OUT, 'metrics_fig5.json'), 'w', encoding='utf-8') as fp:
    json.dump(res, fp, indent=1)
print('\nwrote metrics_fig5.json')
