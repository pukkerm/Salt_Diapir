# MANIFEST

**Salt-diapir controls on the routing of submarine-canyon turbidity currents and their
depositional architecture: insights from numerical modelling**

Fan, H.; Zhang, X.; Liu, K.; Lin, X.; Hu, J.; Li, Z. *Fluids* (MDPI), fluids-4523562.

Package: 90 files, 57.03 MB (59,797,873 bytes).
Companion documents: `README.md` (how to use the package), `PARAMETERS.md` and
`parameters.csv` (the full parameter set and its mapping to Table 1 of the manuscript).

## Directory totals

| Directory | Files | Size |
|---|---|---|
| `(root)` | 8 | 32.2 KB |
| `01_model_configuration/` | 8 | 75.0 KB |
| `01_model_configuration/initial_topography/` | 6 | 25.39 MB |
| `02_figures/ (scripts + common.py)` | 7 | 59.0 KB |
| `02_figures/output/` | 6 | 11.91 MB |
| `02_figures/pipeline/` | 13 | 44.3 KB |
| `03_derived_data/` | 42 | 19.52 MB |

The package is self-contained for the figures. The raw pyBadlands output (about 130 GB) is
not included; `02_figures/pipeline/` rebuilds `03_derived_data/` from it.

## Files

`md5  size (bytes)  path`

The MD5 of this file is not listed, because the list cannot contain its own hash.

```
654a1459ba9bedd0d54b78773459888b        142  .gitignore
210464c9400e183dd93bc0fb05298f95       6900  01_model_configuration/delta_fan.xml
80edf2d1d75b563580aa5a5cd2de5c33       6906  01_model_configuration/delta_fan100.xml
68f6c9a4feeb5901052627e14dd6b2b8       6906  01_model_configuration/delta_fan200.xml
81138fea0cbfa8888ada4be6db6d1b65       6906  01_model_configuration/delta_fan250.xml
ef97f57bbc8458536ef2edaf33d0400c       6906  01_model_configuration/delta_fan300.xml
f4e749681959cd6307a095b2098ade0c       1713  01_model_configuration/export_initial_dem.py
2700bbde6195a4c153721a15397502b7    5325602  01_model_configuration/initial_topography/fan.csv
dea2960f4c34bfda6e6253b566a0cb34    5325203  01_model_configuration/initial_topography/fan100.csv
2b446287d77284c089a67b5700ac4e2f    5324791  01_model_configuration/initial_topography/fan200.csv
5d94b74783dd283373726e45933aa7e9    5324609  01_model_configuration/initial_topography/fan250.csv
ca939645bd012f24fe7fb4fedaf5ab13    5324467  01_model_configuration/initial_topography/fan300.csv
07a9a5f39cec60ee29b1c273f816a353       1375  01_model_configuration/initial_topography/PROVENANCE.txt
0f122c5434233947e5c2884b26effe26      26052  01_model_configuration/paraview_trace.py
0c2f6e6796dbb883a205649263c7415e      14545  01_model_configuration/topoCreate.ipynb
b9a43ff375b311f9a1827268bd74aa7e       6143  02_figures/common.py
e9311941ac32d4bd1fa30ced8327deb2      11073  02_figures/fig1_model_setup.py
c3803fe455a1bdcb5a4ef9616e1189a7       7366  02_figures/fig2_thickness_maps.py
9f3eb874a91db8af247b7ba44cfc9d17      10559  02_figures/fig3_dip_section.py
d4205744a0dd5e4a9da158e13012b1ad      10524  02_figures/fig4_transverse_section.py
12ee86b09b00487f3682f4bfccdb760c       6228  02_figures/fig5_routing_metrics.py
cb2fa8551fc43d5d0a3d74f6315c2c8a       8481  02_figures/fig6_depositional_modes.py
c8f074657a51c0b05a123994421747e4     872047  02_figures/output/Figure 1.png
2552cead929f256e7b107ce40b0ab0a7    3024507  02_figures/output/Figure 2.png
437e4617e25929d5fae8229835e5923b     922395  02_figures/output/Figure 3.png
a0bc7923859fafae729091735d8f2d4c    2903289  02_figures/output/Figure 4.png
e15fc7b7ee0625306ee0cf4932ef8dcb    3907409  02_figures/output/Figure 5.png
60685d9b9068d1882269a9b4acb92246     861085  02_figures/output/Figure 6.png
d7dc6e9da1e11b7019d4fa619f1e4441       2646  02_figures/pipeline/extract_all.py
bb713fc2792fe799c559e601a4b5c919       2310  02_figures/pipeline/extract_dem.py
f242f155a3c9696376fecc79a562408c       2764  02_figures/pipeline/extract_section_wide.py
9411f29a602da61adf3f2eadf4dd604c       4863  02_figures/pipeline/extract_sections.py
a4aba6e74aadc522579c9d98755eaab6       3047  02_figures/pipeline/extract_sections2.py
f501298fe20e42b6510118e36897aca0       3270  02_figures/pipeline/extract_sections3.py
3848ebe18321328ccddf4f8fed2ba3bf       2833  02_figures/pipeline/extract_steps.py
fd853fd4dbf0ce4850694690dc93fe56       3405  02_figures/pipeline/extract_volumes.py
42de4efb1a05d6d391c8a7292c897b70       4507  02_figures/pipeline/metrics.py
2835d49b7474439bdad7d8bcfaa064a0       3213  02_figures/pipeline/metrics2.py
19381f5c59b40bc4f4224893e45b6b0d       4912  02_figures/pipeline/refine_bands.py
71432f296808726086750eb26d983212       4375  02_figures/pipeline/refine_metrics.py
54839a1d81b17f77b1bd46a8c3a1bd4e       3186  02_figures/pipeline/refine_stages.py
83a079c36b60a29895cecb3004bd0b02       3150  03_derived_data/axial_profiles.npz
896fa2bf290dfcbbb298235122dd3823       4190  03_derived_data/bands_fig5.json
b9e23b35ca2117229119ed51fe80f29c     738618  03_derived_data/dem_fan.npz
9bb299f6ee3095de8c2a083507918900     738670  03_derived_data/dem_fan100.npz
e7b984f8f17d7bbe0747e3241196135f     738575  03_derived_data/dem_fan200.npz
2f760b055ec5acc3275456f3e9c4c9ca     738567  03_derived_data/dem_fan250.npz
a2afb3e245115ba6ea0216864c8cf210     738449  03_derived_data/dem_fan300.npz
bbe9376764623d12d91bafc002fc94a8       2699  03_derived_data/dem_grid.npz
51ae417082360d0152b991a58a807846       4644  03_derived_data/meta.json
a1827c0809a56cb92a9a6d80776914ec       8367  03_derived_data/metrics_fig5.json
b559f2b8014deee054fdd5e34093545f       4208  03_derived_data/metrics.json
0ab9a47a4267edd01219854a66b893fb        726  03_derived_data/rates_fig5.json
2a632b2099d7f7e8afacf338e0f97cb5     566792  03_derived_data/sec_fan_xfull.npz
709afa4ffac57890f716174f448af54b     480418  03_derived_data/sec_fan_y160w.npz
09bc3ceed34d0e7063acfa35b26891bc     570311  03_derived_data/sec_fan100_xfull.npz
a4512d856368f9d0a92ceb5e6974452b     476013  03_derived_data/sec_fan100_y160w.npz
c5378cc23935c01cb0bb62486842438a     523535  03_derived_data/sec_fan200_xfull.npz
39bffad9de5c67ba0ee94dd73034a062     473341  03_derived_data/sec_fan200_y160w.npz
0f66da880e211328a9379e5a6fe6c614     431525  03_derived_data/sec_fan250_xfull.npz
9563ab3d87caf2a889ee913bcada1569     424168  03_derived_data/sec_fan250_y160w.npz
c25894ed149db8f4e4e2b7fd7f4907c6     405947  03_derived_data/sec_fan300_xfull.npz
b57350a63bf6cb7b9f5d01bc1c944de7     384562  03_derived_data/sec_fan300_y160w.npz
53bf9c4ded9877e478ac1838e14843f2       9806  03_derived_data/stages_fig5.json
d7765b24fd5ddf39fbb3462069b1faec     796532  03_derived_data/T_step10_fan.npy
4ce5dbecf511afbcc3e7a513b64158a1     796532  03_derived_data/T_step10_fan100.npy
43a06fa25b243986e10fc31230507352     796532  03_derived_data/T_step10_fan200.npy
de8f4358880e966995bf0d04f093310a     796532  03_derived_data/T_step10_fan250.npy
78250a521cf10531984726e8928e4a5e     796532  03_derived_data/T_step10_fan300.npy
296e34dfb0f30fb282ecacc79c70b179     796532  03_derived_data/T_step20_fan.npy
9b286da365428711a1e77e7ec0f0b220     796532  03_derived_data/T_step20_fan100.npy
5db191ac934b27b854c6db735803b2ef     796532  03_derived_data/T_step20_fan200.npy
6ca9569d3902b01fd38795417a68ef60     796532  03_derived_data/T_step20_fan250.npy
673e1d53d5d4633758640bede1f6c969     796532  03_derived_data/T_step20_fan300.npy
10563feae7df0f036846f75230a90f73     796532  03_derived_data/T_step30_fan.npy
30eb365f27069adacd621b5d892d718d     796532  03_derived_data/T_step30_fan100.npy
3d40f2488aa86885c6458a49af1e9820     796532  03_derived_data/T_step30_fan200.npy
b823bb866e2f6ec29fa75d58b9beaec7     796532  03_derived_data/T_step30_fan250.npy
6fafb26a7ab2e0f100e68852f920c9e6     796532  03_derived_data/T_step30_fan300.npy
bff440d68727ffa9fc5967e62fc3382e      41809  03_derived_data/volumes_time.json
6dc1e7a16940d3e706f63d701d712234       1073  03_derived_data/volumes.json
a0b623ef8144f06aad6d28c8283356d6       4120  03_derived_data/xi.npy
d22f45546343d554a0d88e71b29a7b16       3320  03_derived_data/yi.npy
e2e4a55ade74a47846a6ffbb3321fd7d       1122  LICENSE
2bee48a43fb337699339db661be28d6e        978  LICENSE-DATA
4b8c2f1cb613ab443f121a2f0fad6917       2318  parameters.csv
3931672feab977da82de5c560b5cc33d       9149  PARAMETERS.md
9f6a49a7a5e7fd8ee18e9120b1b74b71       9744  README.md
09a759b83059cdb82e3699c32a5d44a6        355  requirements.txt
```

## Changes with respect to the first-round package

- **`dens_cr`** in the five `delta_fan*.xml` files is set to 1070 kg/m3, the value quoted in
  Table 1 of the manuscript. Runs with the threshold at 1040, 1070 and 3000 kg/m3 give the
  same deposited volume, maximum thickness and bypass fraction, so the change does not alter
  any reported result.
- **Removed, the reduced sections that no figure reads** (20 files,
  `sec_<case>_x100|x150|x170|y150|y170.npz`): only `sec_<case>_xfull.npz` (Figure 4) and
  `sec_<case>_y160w.npz` (Figure 5) are used.
- **Removed, the duplicate thickness arrays** (5 files, `thick_<case>.npy`): byte-identical to
  `T_step30_<case>.npy`.
- **Removed, the working check scripts** (7 files, `_chk*.py` in `02_figures/pipeline/` and
  `03_derived_data/`).
- **Fixed in the figure scripts**: the colour bars of Figures 2, 4 and 5 were built from a
  `ScalarMappable` without an array, which raises `TypeError` on matplotlib 3.0 (add
  `set_array([])`); `fig6_depositional_modes.py` used the `fc`/`ec` aliases, which that
  matplotlib rejects (now `facecolor`/`edgecolor`); `fig3_dip_section.py` and
  `fig4_transverse_section.py` still carried the 5 kyr band labels and now read 15 kyr, the
  band interval used in the manuscript. All six scripts now run to completion in the
  pyBadlands container.
- **Added** `PARAMETERS.md`, `parameters.csv`, `LICENSE` (MIT) and `LICENSE-DATA` (CC BY 4.0).
- **README** now lists the licence, the exact pyBadlands version and commit, and the `data/`
  step needed to re-run the model.
