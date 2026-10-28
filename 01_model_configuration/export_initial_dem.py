# ---------------------------------------------------------------------------
# Rebuild an input topographic grid (*.csv) from the model's own stratigraphic
# output.  Use this only when the original data/<case>.csv cannot be found: the
# grid written here is the initial surface sampled on the 500 m stratigraphic
# grid, which is the surface the run actually started from.
# ---------------------------------------------------------------------------
import os
import glob
import numpy as np
import h5py


def _release_root(start):
    d = os.path.dirname(os.path.abspath(start))
    while d and d != os.path.dirname(d):
        if glob.glob(os.path.join(d, '*_derived_data')):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(start))


ROOT_DIR = _release_root(__file__)
RAW = os.environ.get('BADLANDS_OUTPUT', os.path.join(ROOT_DIR, 'raw_badlands_output'))
OUT = os.path.join(ROOT_DIR, '01_model_configuration', 'initial_topography')

CASES = ['fan', 'fan100', 'fan200', 'fan250', 'fan300']

for case in CASES:
    src = os.path.join(RAW, case, 'h5', 'sed.time1.hdf5')
    if not os.path.exists(src):
        print('%-8s missing: %s' % (case, src))
        continue
    with h5py.File(src, 'r') as f:
        coords = np.array(f['coords'], dtype=np.float64)
        z = np.array(f['layElev'][:, 0], dtype=np.float64)
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, '%s.csv' % case)
    with open(dst, 'w') as fh:
        fh.write('X,Y,Z\n')
        for (x, y), zz in zip(coords, z):
            fh.write('%.1f,%.1f,%.3f\n' % (x, y, zz))
    print('%-8s wrote %s  (%d nodes, z %.0f .. %.0f)' % (case, dst, z.size, z.min(), z.max()))

print('DONE')
