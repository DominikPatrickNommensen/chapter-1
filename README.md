# Australian dune whorl code
This code allows to extract dune crest lines for the Australian dune whorl. It is part of Dominik Nommensen's PhD thesis chapter 1 and the publication "Inferred vegetation during Australia’s dune whorl formation" (currently in submission). Co-authors: Jimmy Daynac and Andrew Gunn.

Some data can be accessed via zenodo (link will be provided soon). Other data can be provided upon request.

## Structure

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
│   ├── SKL
│   │   └── Skeleton (SKL) of crest lines (raster)
├── dist (or build)
├── node_modules
├── bower_components (if using bower)
├── test
├── Gruntfile.js/gulpfile.js
├── README.md
├── package.json
├── bower.json (if using bower)
└── .gitignore
```

