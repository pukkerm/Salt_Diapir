# MANIFEST

Complete file listing of the data-and-code release. Sizes are uncompressed.
See `README.md` for what each item is used for.

**Total: 111 files, 67.5 MB.**

## (package root)  —  4 files, 13 KB

- `.gitignore` — 142 B
- `MANIFEST.md` — 5 KB
- `README.md` — 8 KB
- `requirements.txt` — 355 B

## 01_model_configuration/  —  8 files, 75 KB

Model input: the five pyBadlands XML input files, the initial-topography notebook, the DEM export script and the ParaView trace.

- `delta_fan.xml` — 7 KB
- `delta_fan100.xml` — 7 KB
- `delta_fan200.xml` — 7 KB
- `delta_fan250.xml` — 7 KB
- `delta_fan300.xml` — 7 KB
- `export_initial_dem.py` — 2 KB
- `paraview_trace.py` — 25 KB
- `topoCreate.ipynb` — 14 KB

## 01_model_configuration/initial_topography/  —  6 files, 25.4 MB

The five input grids rebuilt from the model's own first stratigraphic layer; see PROVENANCE.txt, and replace them with the original data/fan*.csv if these are found.

- `fan.csv` — 5.1 MB
- `fan100.csv` — 5.1 MB
- `fan200.csv` — 5.1 MB
- `fan250.csv` — 5.1 MB
- `fan300.csv` — 5.1 MB
- `PROVENANCE.txt` — 1 KB

## 02_figures/  —  7 files, 59 KB

One shared style module and the six figure scripts (the file names keep the internal working order, not the published figure order).

- `common.py` — 6 KB
- `fig1_model_setup.py` — 11 KB
- `fig2_thickness_maps.py` — 7 KB
- `fig3_dip_section.py` — 10 KB
- `fig4_transverse_section.py` — 10 KB
- `fig5_routing_metrics.py` — 6 KB
- `fig6_depositional_modes.py` — 8 KB

## 02_figures/pipeline/  —  13 files, 44 KB

Scripts that rebuild 03_derived_data/ from the raw pyBadlands output; they need the raw output and stratalAnalyse (badlands_companion) and are not required to draw the figures.

- `extract_all.py` — 3 KB
- `extract_dem.py` — 2 KB
- `extract_section_wide.py` — 3 KB
- `extract_sections.py` — 5 KB
- `extract_sections2.py` — 3 KB
- `extract_sections3.py` — 3 KB
- `extract_steps.py` — 3 KB
- `extract_volumes.py` — 3 KB
- `metrics.py` — 4 KB
- `metrics2.py` — 3 KB
- `refine_bands.py` — 5 KB
- `refine_metrics.py` — 4 KB
- `refine_stages.py` — 3 KB

## 02_figures/output/  —  6 files, 11.9 MB

The final figure files as submitted (the vector versions finished in CorelDRAW), in published figure order.

- `Figure 1.png` — 852 KB
- `Figure 2.png` — 2.9 MB
- `Figure 3.png` — 901 KB
- `Figure 4.png` — 2.8 MB
- `Figure 5.png` — 3.7 MB
- `Figure 6.png` — 841 KB

## 03_derived_data/  —  67 files, 30.0 MB

The derived data behind every figure: cumulative thickness maps, initial surfaces, sections, volumes and rate/volume metrics. See README section 3 for the keys of each file.

- `axial_profiles.npz` — 3 KB
- `bands_fig5.json` — 4 KB
- `dem_fan.npz` — 721 KB
- `dem_fan100.npz` — 721 KB
- `dem_fan200.npz` — 721 KB
- `dem_fan250.npz` — 721 KB
- `dem_fan300.npz` — 721 KB
- `dem_grid.npz` — 3 KB
- `meta.json` — 5 KB
- `metrics_fig5.json` — 8 KB
- `metrics.json` — 4 KB
- `rates_fig5.json` — 726 B
- `sec_fan_x100.npz` — 382 KB
- `sec_fan_xfull.npz` — 554 KB
- `sec_fan_y150.npz` — 341 KB
- `sec_fan_y160.npz` — 334 KB
- `sec_fan_y160w.npz` — 469 KB
- `sec_fan_y170.npz` — 351 KB
- `sec_fan100_x100.npz` — 384 KB
- `sec_fan100_xfull.npz` — 557 KB
- `sec_fan100_y150.npz` — 355 KB
- `sec_fan100_y160.npz` — 325 KB
- `sec_fan100_y160w.npz` — 465 KB
- `sec_fan100_y170.npz` — 366 KB
- `sec_fan200_x100.npz` — 361 KB
- `sec_fan200_xfull.npz` — 511 KB
- `sec_fan200_y150.npz` — 377 KB
- `sec_fan200_y160.npz` — 307 KB
- `sec_fan200_y160w.npz` — 462 KB
- `sec_fan200_y170.npz` — 374 KB
- `sec_fan250_x100.npz` — 299 KB
- `sec_fan250_xfull.npz` — 421 KB
- `sec_fan250_y150.npz` — 388 KB
- `sec_fan250_y160.npz` — 241 KB
- `sec_fan250_y160w.npz` — 414 KB
- `sec_fan250_y170.npz` — 374 KB
- `sec_fan300_x100.npz` — 289 KB
- `sec_fan300_xfull.npz` — 396 KB
- `sec_fan300_y150.npz` — 389 KB
- `sec_fan300_y160.npz` — 197 KB
- `sec_fan300_y160w.npz` — 376 KB
- `sec_fan300_y170.npz` — 373 KB
- `stages_fig5.json` — 10 KB
- `T_step10_fan.npy` — 778 KB
- `T_step10_fan100.npy` — 778 KB
- `T_step10_fan200.npy` — 778 KB
- `T_step10_fan250.npy` — 778 KB
- `T_step10_fan300.npy` — 778 KB
- `T_step20_fan.npy` — 778 KB
- `T_step20_fan100.npy` — 778 KB
- `T_step20_fan200.npy` — 778 KB
- `T_step20_fan250.npy` — 778 KB
- `T_step20_fan300.npy` — 778 KB
- `T_step30_fan.npy` — 778 KB
- `T_step30_fan100.npy` — 778 KB
- `T_step30_fan200.npy` — 778 KB
- `T_step30_fan250.npy` — 778 KB
- `T_step30_fan300.npy` — 778 KB
- `thick_fan.npy` — 778 KB
- `thick_fan100.npy` — 778 KB
- `thick_fan200.npy` — 778 KB
- `thick_fan250.npy` — 778 KB
- `thick_fan300.npy` — 778 KB
- `volumes_time.json` — 41 KB
- `volumes.json` — 1 KB
- `xi.npy` — 4 KB
- `yi.npy` — 3 KB
