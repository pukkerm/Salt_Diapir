# Data and Code Release

**Salt-diapir controls on the routing of submarine-canyon turbidity currents and their
depositional architecture: insights from numerical modelling**

Fan, H.; Zhang, X.; Liu, K.; Lin, X.; Hu, J.; Li, Z.
*Fluids* (MDPI), manuscript fluids-4523562

This package holds the model configuration, the figure code, the derived data behind every
figure, and the submitted figure files. It is self-contained for the figures: all six can be
regenerated from the ~23 MB derived data set without the raw model output (about 130 GB in
total). The complete parameter set is listed in `PARAMETERS.md` (machine-readable:
`parameters.csv`).

---

## 1. Contents

| Path | What it holds |
|---|---|
| `PARAMETERS.md`, `parameters.csv` | Every model parameter, with the mapping to Table 1 of the manuscript. |
| `01_model_configuration/` | The five pyBadlands input files (`delta_fan*.xml`), the notebook that builds the initial topography (`topoCreate.ipynb`), the initial-DEM export script, and the ParaView trace used to visualise the runs. |
| `01_model_configuration/initial_topography/` | The five input grids, rebuilt from the model output; read `PROVENANCE.txt` there first. |
| `02_figures/` | The shared style module (`common.py`), the six figure scripts (`fig1`…`fig6`), the scripts that rebuild the derived data (`pipeline/`), and the submitted figure files (`output/`). |
| `03_derived_data/` | The derived data: cumulative thickness maps, initial surfaces, two section families, volumes and the metrics behind Figure 3. |
| `LICENSE`, `LICENSE-DATA` | Licence of the code and of the data. |

## 2. Model configuration

Five runs differ **only** in the height of the salt diapir. The canyon depth is 200 m in all
five runs, so *R*df = *H* / *D*c takes the values 0, 0.5, 1.0, 1.25 and 1.5.

| Case | Diapir relief *H* (m) | *R*df | Model in the paper |
|---|---|---|---|
| `fan` | 0 | 0.0 | Model 1 |
| `fan100` | 100 | 0.5 | Model 2 |
| `fan200` | 200 | 1.0 | Model 3 |
| `fan250` | 250 | 1.25 | Model 4 |
| `fan300` | 300 | 1.5 | Model 5 |

Key settings, identical in the five files (full list in `PARAMETERS.md`):

```
grid      demfile data/<case>.csv,  resfactor 1,  boundary slope,  nopit 1
time      start 0 yr,  end 150000 yr,  mindt 1 yr,  display 5000 yr
strata    stratdx 500 m,  laytime 500 yr,  poro0 0.52,  poroC 0.47 /km
sea       position 0 m
rain      rstart 0 yr,  rend 150000 yr,  rval 2 m/yr
sp_law    dep 1,  slp_cr 0.001,  perc_dep 0.5,  m 0.5,  n 1.0,  erodibility 2e-6
          diffnb 10,  diffprop 0.01,  dens_cr 1070 kg/m3,  deepbasin -200 m
creep     caerial 0.3,  cmarine 0.5,  criver 10 m2/yr
```

The stratigraphic output grid is regular, 499 x 399 nodes at 500 m spacing, covering
X = 0-249 km and Y = 0-199 km; the 0.5 kyr layer interval gives 301 layers over the 150 kyr
run. The sea floor is resolved by the model TIN (about 39 800 nodes, mean edge length
1.26 km). The run is driven by constant precipitation only: no wave, tidal, wind or
baroclinic forcing is applied, the tectonic block is commented out, and the model does not
solve the hydrodynamic equations.

The density threshold `dens_cr` = 1070 kg/m3 is a prescribed closure. Runs with the
threshold at 1040, 1070 and 3000 kg/m3 give the same deposited volume, maximum thickness and
bypass fraction, so the reported results do not depend on this value.

## 3. Derived data (`03_derived_data/`)

| Files | Content |
|---|---|
| `T_step10/20/30_<case>.npy` | Cumulative sediment thickness at Steps 10, 20 and 30 (50, 100 and 150 kyr), one array per case, 499 x 399. Used by Figure 2. |
| `dem_<case>.npz` | Initial topographic surface of each case, keys `z`, `xi`, `yi`, `H`. Used by Figure 1. |
| `dem_grid.npz` | Grid definition of the initial surfaces. |
| `sec_<case>_xfull.npz` | Dip-directed section along the canyon axis (X = 140-180 km, flattened on the present-day sea floor). Used by Figure 4. |
| `sec_<case>_y160w.npz` | Transverse section at X = 160 km (Y = 70-130 km, true elevation). Used by Figure 5. |
| `xi.npy`, `yi.npy` | Coordinate vectors of the stratal grid (metres). |
| `axial_profiles.npz` | Axial thickness profiles used by Figure 3. |
| `volumes.json`, `volumes_time.json` | Preserved volume through time (axial corridor, flanks, beyond the diapir, total). |
| `metrics.json` | The metrics plotted in Figure 3. |
| `metrics_fig5.json`, `bands_fig5.json`, `stages_fig5.json`, `rates_fig5.json` | The band, stage and rate tables behind the numbers quoted for the sections in Figures 4 and 5. |
| `meta.json` | Grid definition and per-section extrema. |

The section files hold the keys `dist`, `secDep` (301 layers), `secTh`, `coord` and `H`.
One stratal cell is 0.25 km2 (500 m x 500 m); volumes are reported in km3 and the
width-normalised deposition rate in km2/yr.

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
| `fig5_routing_metrics.py` | Figure 3 | Axial and flank thickness, thickness ratio, preserved volumes and deposition rate. |
| `fig3_dip_section.py` | Figure 4 | Dip-directed (longitudinal) sections along the canyon axis. |
| `fig4_transverse_section.py` | Figure 5 | Transverse sections at X = 160 km. |
| `fig6_depositional_modes.py` | Figure 6 | Conceptual depositional modes (drawn from the metrics, no gridded input). |

The scripts find the data automatically: the derived-data folder is located next to the
script, so the package can be unpacked anywhere. Four environment variables override the
defaults:

| Variable | Default | Meaning |
|---|---|---|
| `EXTRACT_DIR` | `03_derived_data/` | Folder with the derived data. |
| `BADLANDS_OUTPUT` | `raw_badlands_output/` | Folder with the raw pyBadlands output (needed only to rebuild the derived data). |
| `FIG_OUT` | `out/` | Output folder for the regenerated figures. |
| `STRATAL_DIR` | (unset) | Folder that holds `stratalAnalyse.py` (needed only by `pipeline/`). |

Each script writes PDF, PNG, SVG and TIFF versions of its figure. The six scripts were run
end to end in the pyBadlands container (`badlandsmodel/badlands:latest`, Python 3.5,
matplotlib 3.0) to check that they resolve their data and complete. `02_figures/output/`
holds the figures as submitted, which are the script output after the panel lettering and
the colour-bar labels were finished by hand; the regenerated files therefore match them in
content but not always in typography.

The scripts in `02_figures/pipeline/` rebuild `03_derived_data/` from the raw model output.
They need the raw output plus `stratalAnalyse` (the `badlands_companion` toolbox of the
pyBadlands tools, not included here) and are not required to draw the figures.

## 5. Re-running the forward model

The XML files expect a folder layout of the form

```
<work>/
  delta_fan.xml ...
  data/fan.csv  data/fan100.csv  data/fan200.csv  data/fan250.csv  data/fan300.csv
```

so the grids of `01_model_configuration/initial_topography/` have to be copied to
`data/` under the case names first:

```bash
mkdir data
cp 01_model_configuration/initial_topography/fan.csv     data/fan.csv
cp 01_model_configuration/initial_topography/fan100.csv  data/fan100.csv
cp 01_model_configuration/initial_topography/fan200.csv  data/fan200.csv
cp 01_model_configuration/initial_topography/fan250.csv  data/fan250.csv
cp 01_model_configuration/initial_topography/fan300.csv  data/fan300.csv
cp 01_model_configuration/delta_fan*.xml .
badlands -i delta_fan.xml
```

The same run through the Python API:

```python
from badlands.model import Model as badlandsModel

model = badlandsModel()
model.load_xml('delta_fan.xml')
model.run_to_time(150000)
```

The runs need pyBadlands **v2.3.1** (commit `975f595ae313dd08d674c0effde18b5e8155f997`).
A single run takes about 30 min and about 2 GB of memory.

## 6. What is not in this package

- **The raw pyBadlands output** (about 130 GB for the five runs). `03_derived_data/` holds
  everything the figures read; `02_figures/pipeline/` rebuilds it from the raw output.
- **The original input grids.** The `data/fan*.csv` files used for the runs were not
  archived. `01_model_configuration/initial_topography/` holds five grids rebuilt from the
  base of the first stratigraphic layer of each run, which reproduce the initial surface the
  runs started from on the 500 m stratal grid, but not the 1 km DEM that was used as input.
  A re-run from them therefore follows the same configuration but does not reproduce the
  published numbers exactly; see `PROVENANCE.txt` in that folder.
- **The sensitivity runs behind Figures S1-S6** of the Supplementary Materials. Each one is
  the `fan200` configuration with a single parameter changed; `PARAMETERS.md` §6 lists the
  change for each run, so they can be repeated from the files here.
- **`badlands_companion`** (`stratalAnalyse`), which is part of the pyBadlands tool set.

## 7. Licence and contact

The code is released under the MIT licence (`LICENSE`), the data under CC BY 4.0
(`LICENSE-DATA`).

Corresponding authors: Xu Zhang and Zhuang Li.
