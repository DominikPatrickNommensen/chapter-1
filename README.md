# Australian dune whorl code
This code allows to extract dune crest lines for the Australian dune whorl and further analysis. It is part of Dominik Nommensen's PhD thesis chapter 1 and the publication "Inferred vegetation during Australia’s dune whorl formation" (currently in submission). Co-authors: Jimmy Daynac and Andrew Gunn.

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

## Order of operation

### Step 1 - Download digital surface model:
get-OpenTopo contains:
- *GetOpenTopo.py*: a helper Class to request the desired geotiff from OpenTopography (https://opentopography.org/)
- download_opentopo.ipynb: notebook to specify the extend of geotiff(s) and handle download to specified folder location

### Step 2 – Extract the crest lines for the Australian dune whorl:
extract-crest-lines contains:
- extract-lines-COP30.ipynb: This notebook is used to extract the residual relief (RR) from topography, calculate volumetric obscurance (VO) from RR, crop the VO by a dune mask and perform a top-down skeletonization process to generate dune crestlines as vectors following Daynac et al. 2024 (10.1016/j.geomorph.2024.109369 ) with code from Rolland et al. 2022 (doi.org/10.3390/rs14040941) and Tveite 2017 (https://github.com/havatv/qgisthingreyscaleplugin).

### Step 3 – Extract dune parameters from topography and crestlines:
extract-topo contains:
- YjunctionClass.py: a helper Class to extract the bisector and opening angle(s) of a yjunction defined.
- 01_topography.iypnb: This notebook is used to calculate the direction, spacing, interaction index, slopes, y-junction bisectors and other related parameters of dunes within a 0.1x0.1° cell (equivalent to the ERA5-Land grid).
- 02_build_inventory.ipynb: Quick notebook to combine the most important parameters for this study into dataframe and save a netcdf

### Step 4 - Generating ERA5 winds on ERA5-Land grid, calculate the bedmodes for the whorl and find optimal threshold velocity
- Era5-land_1950)2025_uam10_hist.zarr: Era5 interpolated wind histogram for 76 years of reanalysis winds
- create-histograms-era5-land.ipynb: This notebook is used to interpolate ERA5 to ERA5-land grid based on findings by Baas 2026 (doi.org/10.1016/j.apenergy.2026.127634) to create wind direction and wind speed histograms for 76 years if ERA5 reanalysis winds for the eintire planet.
- mask.nc: ERA5-land (0.1x0.1° grid) land mask
- calculate-modes-from-era5-and-topo: Notebook to calculate the bedmodes, saturated sand flux parameters (Courrech du Pont et al. 2024; doi.org/10.1016/j.earscirev.2024.104772) and find the optimal threshold speed for variable dune slopes
- calculate-modes-from-era5-and-topo-fixed: Notebook to calculate the bedmodes, saturated sand flux parameters (Courrech du Pont et al. 2024; doi.org/10.1016/j.earscirev.2024.104772) and find the optimal threshold speed for fixed dune slopes
- era5-land_1950_2025_bedmodes_dynamic_dm.nc & era5-land_1950_2025_bedmodes_fixed_dm.nc: Calculated bedmodes from variable and fixed slopes
- era5-land_1950_2025_qsat_dynamic_dm.nc & era5-land_1950_2025_qsat_fixed_dm.nc: saturated sand flux paramters from variable and fixed slopes
- era5-land_1950_2025_ut_opt_dynamic_dm.nc & era5-land_1950_2025_ut_opt_fixed_dm.nc: combined dataset including the optimal threshold velocity for variable and fixed slopes

### Step 5 – plot data:
- look-plots.ipynb: Notebook to combine all relevant datasets and generate paper plots
- dune_atlas.nc: main dataset for analysis
- RaPP-andrew.nc Spatially averaged monthly GEOGLAM Rangeland and Pasture Productivity (RaPP) fractional vegetation cover (original dataset: doi.org/10.4225/08/5848a3f19a7b3) 
- paper_ready_plots: folder containing publication figures as png and pdf files
- example_cell: folder with single 0.1x0.1° cell examples 

