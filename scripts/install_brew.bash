#!/usr/bin/env bash

read -p "Are you sure to install brew? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

brew tap osgeo/osgeo4mac

brew install git
brew cask install xquartz
brew install cmake
brew install create-dmg

# pyproj has bug for python3, unable to install from pip3
pip3 install python-dateutil
pip3 install cython
pip3 install git+https://github.com/jswhit/pyproj.git

brew install openvpn
brew install szip
brew install hdf5
brew link --overwrite numpy
brew install scipy
brew install netcdf
brew install gsl
brew install exiv2

# make sure you do not install homebrew-core/gdal since it
# does not support netcdf
brew install osgeo/osgeo4mac/gdal2 --with-complete --with-libkml
brew install osgeo/osgeo4mac/saga-gis-lts
brew install grass7
brew install gdal2-python

# use this link until postgis is build on osgeo
brew uninstall gdal # safety
brew link gdal2 --force
brew install https://raw.githubusercontent.com/OSGeo/homebrew-osgeo4mac/530a838c9d93721d0c2d5eee2ddeb702b848184f/Formula/postgis.rb --build-from-source


# tools
pip3 install dropbox
pip3 install GitPython

pip3 install owslib

# qgis deps
brew install qgis3 --only-dependencies

# extra python stuff

# part of osgeo4w, but
# not found for pip3
# pip3 install core
# pip3 install gdal-dev
# pip3 install pypiwin32
# pip3 install python-help
# pip3 install python-tcltk
# pip3 install python3-devel
# pip3 install pywin32
# pip3 install wx

# Not sure here, we have brew package for qscintilla already with sip
# pip3 install qscintilla

pip3 install certifi
pip3 install chardet
pip3 install coverage
pip3 install cycler
pip3 install decorator
pip3 install exifread
pip3 install future
pip3 install future
pip3 install gdal
pip3 install h5py
pip3 install httplib2
pip3 install idna
pip3 install ipython-genutils
pip3 install jinja2
pip3 install jsonschema
pip3 install jupyter-core
pip3 install kiwisolver
pip3 install markupsafe
pip3 install matplotlib
pip3 install mock
pip3 install mock
pip3 install nbformat
pip3 install networkx
pip3 install nose2
pip3 install numpy
pip3 install owslib
pip3 install pandas
pip3 install pbr
pip3 install pip
pip3 install plotly
pip3 install ply
pip3 install psycopg2
pip3 install pygments
pip3 install pyodbc
pip3 install pyparsing
pip3 install pypubsub
pip3 install pysal
pip3 install pytz
pip3 install pyyaml
pip3 install requests
pip3 install retrying
pip3 install scipy
pip3 install setuptools
pip3 install shapely
pip3 install simplejson
pip3 install six
pip3 install test
pip3 install tools
pip3 install traitlets
pip3 install urllib3
pip3 install xlrd
pip3 install xlwt
