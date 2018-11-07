#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

TAG=${final-3_4_1}
BD=$DIR/../builds/pr-${TAG}

echo "BUILDING PR"
mdir -p $BD

$DIR/run_build.bash \
  $BD \
  $TAG \
  pr