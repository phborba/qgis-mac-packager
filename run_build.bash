#!/bin/bash

set -e

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

PWD=`pwd`
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if (( $# != 3 )); then
    echo "run_all build_dir git_tag release_name"
fi

BUILD_DIR=$1
GIT=$2
RELEASE=$3
echo "Building & Packaging QGIS to $BUILD_DIR"
mkdir -p $BUILD_DIR

echo "Building QGIS $GIT for $RELEASE"

echo "Please run brew update manually to get new deps"

cd qgis-mac-packager
echo "Run build"
python3 qgis_builder.py \
  --output_directory $BUILD_DIR \
  --git $GIT

echo "Bundle"
python3 qgis_bundler.py \
  --qgis_install_tree $BUILD_DIR/install  \
  --output_directory $BUILD_DIR/bundle  \
  --python /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Python \
  --pyqt /usr/local/Cellar/pyqt/5.10.1_1/lib/python3.7/site-packages/PyQt5

echo "Package"
python3 qgis_packager.py \
  --bundle_directory $BUILD_DIR/bundle \
  --outname=$BUILD_DIR/qgis_${RELEASE}_${GIT}_${TIMESTAMP}.dmg

echo "Upload"
python3 qgis_uploader.py \
  --dropbox=$DIR/../dropbox_token.txt \
  --destination=/$RELEASE \
  --package=$BUILD_DIR/qgis_${RELEASE}_${GIT}_${TIMESTAMP}.dmg

echo "All done"
cd $PWD