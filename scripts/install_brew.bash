#!/usr/bin/env bash

read -p "Are you sure to install brew? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap osgeo/osgeo4mac

brew install git
brew cask install xquartz
brew install cmake
brew install create-dmg

brew install openvpn
brew install szip
brew install hdf5
brew install cython
brew link --overwrite numpy
brew install scipy
brew install netcdf
brew install grass7
brew install gsl
brew install osgeo/osgeo4mac/saga-gis-lts
brew install exiv2
brew install osgeo/osgeo4mac/gdal2 --with-complete --with-libkml

# python
pip3 install future
pip3 install numpy
pip3 install psycopg2
pip3 install matplotlib
pip3 install pyparsing
pip3 install requests
pip3 install mock
pip3 install pyyaml
pip3 install nose2

pip3 install cython
pip3 install git+https://github.com/jswhit/pyproj.git
pip3 install owslib

# tools
pip3 install dropbox
pip3 install GitPython


brew install qgis3 --only-dependencies