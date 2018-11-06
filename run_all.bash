#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo "Run brew"
# manually?

echo "Run build"
# todo

echo "Bundle"
cd bundler
python3 qgis_bundler.py \
  --qgis_install_tree $DIR/../Applications \
  --output_directory $DIR/build \
  --python /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Python \
  --pyqt /usr/local/Cellar/pyqt/5.10.1_1/lib/python3.7/site-packages/PyQt5
cd $DIR

echo "Package"
cd packager
python3 qgis_packager.py \
  --output_directory $DIR/build \
  --timestamp $TIMESTAMP
cd $DIR

echo "Upload"
cd uploader
python3 qgis_uploader.py \
  --dropbox=$DIR/../dropbox_token.txt \
  --destination=/Nightly
  --package=$DIR/build/qgis_${TIMESTAMP}.dmg

echo "All done"
