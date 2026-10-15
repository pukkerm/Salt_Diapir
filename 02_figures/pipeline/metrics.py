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
"""Quantitative routing metrics for the five static-relief experiments."""
import os, json
import numpy as np
EX = EXTRACT
CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']
H = {'fan': 0, 'fan100': 100, 'fan200': 200, 'fan250': 250, 'fan300': 300}
RDF = {'fan': 0.0, 'fan100': 0.5, 'fan200': 1.0, 'fan250': 1.25, 'fan300': 1.5}
xi = np.load(os.path.join(EX, 'xi.npy')) / 1000.0
yi = np.load(os.path.join(EX, 'yi.npy')) / 1000.0
XX, YY = np.meshgrid(xi, yi)
CELL = 0.25  # km2 per cell

def mask(x0, x1, y0, y1):
    return (XX >= x0) & (XX <= x1) & (YY >= y0) & (YY <= y1)

M_LOCAL = mask(130, 200, 65, 135)
M_ELL = ((XX - 160.0) / 10.0) ** 2 + ((YY - 100.0) / 20.0) ** 2 <= 1.0
M_AXIAL = mask(168, 200, 88, 112)
M_FLANK_N = mask(150, 185, 70, 86)
M_FLANK_S = mask(150, 185, 114, 130)
M_BEYOND = mask(175, 250, 65, 135)
M_DISTAL = mask(165, 250, 65, 135)

rows = []
for case in CASES:
    T = np.load(os.path.join(EX, 'T_step30_%s.npy' % case))
    eps = 1e-9
    r = dict(case=case, H=H[case], Rdf=RDF[case])
    r['Tmax_window'] = float(T[M_LOCAL].max())
    r['T_axial'] = float(T[M_AXIAL].mean())
    r['T_flankN'] = float(T[M_FLANK_N].mean())
    r['T_flankS'] = float(T[M_FLANK_S].mean())
    r['T_flank'] = 0.5 * (r['T_flankN'] + r['T_flankS'])
    r['T_ellipse'] = float(T[M_ELL].mean())
    r['Tmax_ellipse'] = float(T[M_ELL].max())
    outside = M_LOCAL & (~M_ELL)
    r['T_outside'] = float(T[outside].mean())
    r['enrichment'] = r['T_ellipse'] / (r['T_outside'] + eps)
    r['flank_axial_ratio'] = r['T_flank'] / (r['T_axial'] + eps)
    Vloc = float((T[M_LOCAL] * CELL).sum())
    Vby = float((T[M_BEYOND] * CELL).sum())
    r['V_local'] = Vloc
    r['V_beyond175'] = Vby
    r['bypass_frac'] = Vby / (Vloc + eps)
    w = T[M_LOCAL] + eps
    r['Xc_local'] = float((w * XX[M_LOCAL]).sum() / w.sum())
    w2 = T[M_DISTAL] + eps
    r['Xc_distal'] = float((w2 * XX[M_DISTAL]).sum() / w2.sum())
    r['migration'] = r['Xc_local'] - 130.0
    for ts in (10, 20):
        Tt = np.load(os.path.join(EX, 'T_step%02d_%s.npy' % (ts, case)))
        r['T_axial_s%d' % ts] = float(Tt[M_AXIAL].mean())
        r['Xc_local_s%d' % ts] = float(((Tt[M_LOCAL] + eps) * XX[M_LOCAL]).sum() / (Tt[M_LOCAL] + eps).sum())
        r['V_local_s%d' % ts] = float((Tt[M_LOCAL] * CELL).sum())
    rows.append(r)

hdr = ['Rdf', 'Tmax_win', 'T_axial', 'T_flank', 'T_ell', 'T_out', 'enrich', 'flank/ax', 'V_loc', 'V_by175', 'byp_frac', 'Xc_loc', 'Xc_dist']
print('  '.join('%-9s' % h for h in hdr))
for r in rows:
    print('%-9.2f%-9.1f%-9.2f%-9.2f%-9.1f%-9.2f%-9.2f%-9.2f%-9.1f%-9.1f%-9.3f%-9.2f%-9.2f' % (
        r['Rdf'], r['Tmax_window'], r['T_axial'], r['T_flank'], r['T_ellipse'], r['T_outside'],
        r['enrichment'], r['flank_axial_ratio'], r['V_local'], r['V_beyond175'], r['bypass_frac'],
        r['Xc_local'], r['Xc_distal']))
print()
for r in rows:
    print('Rdf=%.2f  axial step10=%.2f step20=%.2f step30=%.2f | Xc_local 10=%.1f 20=%.1f 30=%.1f | Vloc 10=%.1f 20=%.1f 30=%.1f' % (
        r['Rdf'], r['T_axial_s10'], r['T_axial_s20'], r['T_axial'], r['Xc_local_s10'], r['Xc_local_s20'], r['Xc_local'],
        r['V_local_s10'], r['V_local_s20'], r['V_local']))
with open(os.path.join(EX, 'metrics.json'), 'w', encoding='utf-8') as fp:
    json.dump(rows, fp, indent=1)
print('saved metrics.json')
