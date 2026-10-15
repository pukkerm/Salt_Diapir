# Data and Code Release

**Salt-diapir controls on the routing of submarine-canyon turbidity currents and their
depositional architecture: insights from numerical modelling**

Fan, H., Zhang, X., Liu, K., Lin, X., Hu, J., Li, Z.
*Fluids* (MDPI), manuscript fluids-4523562 — first revision.

This package contains the model configuration, the figure code, the derived data behind
every figure, and the figure files of the study. It is self-contained: all six figures can
be regenerated from the ~30 MB derived data set without the raw model output (about 130 GB
in total).

---

## 1. Contents

| Folder | What it holds |
|---|---|
| `01_model_configuration/` | The five pyBadlands XML input files (`delta_fan*.xml`), the notebook that builds the initial topography (`topoCreate.ipynb`), the initial-DEM export script and the ParaView trace script used to visualise the runs. |
| `02_figures/` | The shared style module (`common.py`), the six figure scripts (`fig1`…`fig6`), the scripts that rebuild the derived data (`pipeline/`) and the submitted figure files (`output/`). |
| `03_derived_data/` | The derived data: cumulative thickness maps, initial surfaces, sections, volumes and rate/volume metrics. |

## 2. Model configuration

Five runs differ **only** in the height of the salt diapir (0, 100, 200, 250, 300 m for
`fan`, `fan100`, `fan200`, `fan250`, `fan300`). Every other parameter is identical, so the
five runs isolate the topographic relief as a single variable.

Key settings in `delta_fan*.xml`:

```
grid      demfile data/<case>.csv,  resfactor 1,  boundary slope,  nopit 1
time      start 0 yr,  end 150000 yr,  mindt 1 yr,  display 5000 yr
strata    stratdx 500 m,  laytime 500 yr,  poro0 0.52,  poroC 0.47
sea       position 0 m
rain      rstart 0 yr, rend 150000 yr, rval 2 m/yr
sp_law    dep 1, slp_cr 0.001, perc_dep 0.5, m 0.5, n 1.0, erodibility 2e-6
          diffnb 10, diffprop 0.01, dens_cr 1040 kg/m3, deepbasin -200 m
creep     caerial 0.3, cmarine 0.5, criver 10 m2/yr
```

The stratigraphic output grid is regular, 499 x 399 nodes at 500 m spacing, covering
X = 0-249 km and Y = 0-199 km; the alternating (0.5 kyr) stratigraphic layer interval
produces 301 layers over the 150 kyr run. The sea floor is resolved by the model TIN
(about 40 000 nodes), and the run is driven by constant precipitation only: no wave,
tidal, wind or baroclinic forcing is applied, and the model does not solve the
hydrodynamic equations.

## 3. Derived data (`03_derived_data/`)

| Files | Content |
|---|---|
| `T_step10/20/30_<case>.npy` | Cumulative sediment thickness at Steps 10, 20 and 30 (50, 100 and 150 kyr), one array per case. Used by Figure 2. |
| `thick_<case>.npy` | Final cumulative thickness (Step 30). |
| `dem_<case>.npz` | Initial topographic surface of each case (stratal grid), keys `z`, `xi`, `yi`, `H`. |
| `sec_<case>_*.npz` | Cross- and along-strike sections, keys `dist`, `secDep` (301 layers), `secTh`, `coord`, `H`. |
| `xi.npy`, `yi.npy` | Coordinate vectors of the stratal grid (metres). |
| `axial_profiles.npz`, `dem_grid.npz` | Axial thickness profiles and the grid definition. |
| `volumes_time.json`, `volumes.json` | Preserved volume through time (axial corridor, flanks, beyond the diapir, total). |
| `metrics.json`, `metrics_fig5.json`, `bands_fig5.json`, `stages_fig5.json`, `rates_fig5.json`, `meta.json` | The quantitative metrics plotted in Figure 3 and the band/stage data of the sections; `meta.json` records the grid and per-section extrema. |

The area of one stratal cell is 0.25 km2 (500 m x 500 m); all volumes are reported as
km3, and the width-normalised deposition rate as km2/yr.

## 4. Reproducing the figures

```bash
pip install -r requirements.txt
python 02_figures/fig1_model_setup.py               # Figure 1
python 02_figures/fig2_thickness_maps.py            # Figure 2
python 02_figures/fig5_routing_metrics.py           # Figure 3
python 02_figures/fig3_dip_section.py               # Figure 4
python 02_figures/fig4_transverse_section.py        # Figure 5
python 02_figures/fig6_depositional_modes.py        # Figure 6
```

The script names keep the internal working order, which is not the published figure order:

| Script | Manuscript figure | Content |
|---|---|---|
| `fig1_model_setup.py` | Figure 1 | Initial topography, canyon and diapir geometry. |
| `fig2_thickness_maps.py` | Figure 2 | Cumulative thickness maps at 50, 100 and 150 kyr for the five cases. |
| `fig5_routing_metrics.py` | Figure 3 | Axial-corridor and flank thickness, thickness ratio, preserved volumes and deposition rate. |
| `fig3_dip_section.py` | Figure 4 | Dip-directed (longitudinal) sections along the canyon axis. |
| `fig4_transverse_section.py` | Figure 5 | Transverse sections at X = 160 km. |
| `fig6_depositional_modes.py` | Figure 6 | Conceptual depositional modes. |

The scripts find the data automatically: the derived-data folder is located next to the
script, so the package can be unpacked anywhere. Three environment variables override the
defaults:

| Variable | Default | Meaning |
|---|---|---|
| `EXTRACT_DIR` | `03_derived_data/` | Folder with the derived data. |
| `BADLANDS_OUTPUT` | `raw_badlands_output/` | Folder with the raw pyBadlands output (needed only to rebuild the derived data). |
| `FIG_OUT` | `02_figures/out/` | Output folder for the regenerated figures. |
| `STRATAL_DIR` | (unset) | Folder that holds `stratalAnalyse.py` (needed only by `pipeline/`). |

Each script writes PDF, PNG, SVG and TIFF versions of its figure. The SVG files keep the
text as editable text (`svg.fonttype = 'none'`), so the panels can be finished in a vector
editor. Figure 5 was re-plotted from this package on a clean machine (Python 3.10,
matplotlib 3.8.4, numpy 1.21.6, h5py 3.16.0) to confirm that the release is self-contained.
`02_figures/output/` holds the final figure files as submitted, that is, the vector
versions finished in CorelDRAW.

The scripts in `02_figures/pipeline/` rebuild `03_derived_data/` from the raw model output.
They need the raw output plus `stratalAnalyse` (the `badlands_companion` toolbox that ships
with the pyBadlands/ETL tools, not included here), and they are not required to draw the
figures.

## 5. Re-running the forward model

The five XML files are run from a folder that contains both the XML files and
`data/<case>.csv`:

```bash
badlands -i delta_fan.xml
```

The same run through the Python API:

```python
from badlands.model import Model as badlandsModel

model = badlandsModel()
model.load_xml('delta_fan.xml')
model.run_to_time(150000)
```

The runs need pyBadlands (**version/commit to be added**) and the input topographic grids
`data/fan.csv`, `data/fan100.csv`, `data/fan200.csv`, `data/fan250.csv` and
`data/fan300.csv`. The five grids differ only in the height of the elliptical dome that
represents the diapir (20 km x 40 km, centred at X = 160 km, Y = 100 km). The 8 km wide
canyon is cut at X = 130 km, Y = 100 km, and the water-loaded basin deepens eastward to
about -2500 m.

## 6. To be added before deposition

- `data/fan*.csv` — the five **original** input topographic grids. They were not archived
  with the model output and could not be recovered, so they are not part of the reported
  runs' record. The folder `01_model_configuration/initial_topography/` holds five grids
  rebuilt from the model's own first stratigraphic layer by
  `01_model_configuration/export_initial_dem.py`; `PROVENANCE.txt` there explains what
  they are and why a re-run from them will not reproduce the published numbers exactly.
  Replace them with the original files if these are found.
- the pyBadlands version or git commit used for the runs;
- the licence chosen for the code;
- the DOI of this deposit, and the tagged repository release quoted in the paper.

## 7. Contact

Corresponding authors: Xu Zhang and Zhuang Li.
