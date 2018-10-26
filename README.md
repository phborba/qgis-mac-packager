# qgis-mac-packager

Set of scripts to create MacOS QGIS package (pkg) file

The aim is to be able to create standalone QGIS installation 
with ALL dependencies (qt, pyqt, gdal, ...) bundled inside QGIS.app

# Steps

1. Install homebrew and follow steps on homebrew-osgeo4mac to install qgis3
2. Download QGIS git repository
3. Build release version and install it to your local folder
4. Run `python qgis-bundler.py` with python3 and with some reasonable parameters (see `run_bundler.sh`)
5. This will create .pkg file with 

# Notes

- QGIS should be built with QGIS_MACAPP_BUNDLE=0
- In principle it should work with conda deps, but not tested
- This can be probably a replacement of envisioned QGIS_MACAPP_BUNDLE=3 level (qgis/QGIS/mac/*.cmake scripts)

# TODO
- refactor and clean scripts, add docs
- create scripts for running/building 3.4 and nightly release (mac server on cloud)
- implement package signing
- distribute the packages
