#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo "BUILDING NIGHTLY"
$DIR/run_build.bash \
  $DIR/../builds/nightly \
  master \
  nightly