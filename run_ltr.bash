#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

TAG=ltr-3_4
BD=$DIR/../builds/ltr-${TAG}

echo "BUILDING LTR"
$DIR/run_build.bash \
  $BD \
  ${TAG} \
  ltr
