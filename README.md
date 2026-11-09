# Australian dune whorl code
This code allows to extract dune crest lines for the Australian dune whorl. It is part of Dominik Nommensen's PhD thesis chapter 1 and the publication "Inferred vegetation during Australia’s dune whorl formation" (currently in submission). Co-authors: Jimmy Daynac and Andrew Gunn.

Some data can be accessed via zenodo (link will be provided soon). Other data can be provided upon request.

## Structure
Below is the general structure of the repository and the order in which to use the notebooks. This repo does not contain the majority of the files.

```bash
├── Data
│   ├── Copernicus_OpenTopo_Australia
│   │   └── COP30 topograhy data
│   ├── Crestlines
│   │   └── dune whorl related shapefiles and CSVs
│   ├── Daynac_dune_mask
│   │   └── Australian dune mask (raster) based on Daynac et al. 2024
│   ├── Netcdfs
│   │   └── aus_dune_topo.nc (dune topography paramters)
│   ├── RR
│   │   └── residual relief (RR) from topography
│   ├── VO
│   │   └── volumetric obscurance (VO) from residual relief
│   └── SKL
│       └── Skeleton (SKL) of crest lines (raster)
├── extract-crest-lines
│   └── extract-lines-COP30.ipynb
├── extract-topo
│   ├── 01_topograhphy.ipynb
│   ├── 02_build_inventory.ipynb
│   └── YjunctionClass.py
├── get-ERA5-winds
│   ├── calculate-mode-from-era5-and-topo.ipynb
│   ├── calculate-mode-from-era5-and-topo-fixed_dm.ipynb
│   ├── create-histograms-era5-land.ipynb
│   ├── era5-land_1950_2025_ut_opt_fixed_dm.nc
│   ├── era5-land_1950_2025_qsat_fixed_dm.nc
│   ├── era5-land_1950_2025_bedmodes_fixed_dm.nc
│   ├── era5-land_1950_2025_ut_opt_dynamic_dm.nc
│   ├── era5-land_1950_2025_qsat_dynamic_dm.nc
│   ├── era5-land_1950_2025_bedmodes_dynamic_dm.nc
│   ├── mask.nc
│   └── era5-land_1950_2025_uam10_hist.zarr
│       └── wind histogram data
├── get-OpenTopo
│   ├── download_opentopo.ipynb
│   └── GetOpenTopo.py
└── paper-plots
    ├── dune_atlas.nc
    ├── look-plots.ipynb
    ├── RaPP-andrew.nc
    ├── example_cell
        └── raster and vector data of example grid cell
    └── paper_ready_plots
        └── png and pdf versions of figures
```

