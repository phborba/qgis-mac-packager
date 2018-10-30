#!/usr/bin/env bash


/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap osgeo/osgeo4mac
brew install git
brew install openvpn
brew install szip
brew install hdf5
brew install cython
brew link --overwrite numpy
brew install scipy
brew install netcdf
brew install qgis3
