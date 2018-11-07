#!/bin/bash

# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BD=$DIR/../../builds/nightly
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG=$BD/build_${TIMESTAMP}.log

echo "BUILDING NIGHTLY"
mkdir -p $BD

$DIR/run_build.bash \
  $BD \
  master \
  nightly \
2>&1 | tee $LOG

exit_status=$?
if [ $exit_status -eq 0 ]; then
    echo "SUCCESS" | tee -a $LOG
else
    echo "FAIL" | tee -a $LOG
    if [ $QGIS_CRONJOB -eq 1 ]; then
        echo "Your nighly QGIS MacOS Build failed. I am so sorry for that. I will try do better next time." | mail -s "MacOS Build Failure" info@lutraconsulting.co.uk -A $LOG
    fi
fi
exit $exit_status