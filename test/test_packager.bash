#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

python3 $DIR/../qgis-mac-packager/qgis_packager.py --outname $DIR/../../builds/nightly/testbuidle.dmg \
--bundle_directory $DIR

open $DIR/../../builds/nightly/testbuidle.dmg
