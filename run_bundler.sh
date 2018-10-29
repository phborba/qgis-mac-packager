#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

python qgis-bundler.py \
  --qgis_install_tree $DIR/../Applications \
  --output_directory $DIR/build \
  --python /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Python \
  --pyqt /usr/local/Cellar/pyqt/5.10.1_1/lib/python3.7/site-packages/PyQt5 "$@"