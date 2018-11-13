#!/usr/bin/env bash

set -o pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BD=$DIR/builds
LD=$DIR/logs
LOG=$LD/qgis_${TIMESTAMP}.log
SD=$DIR/qgis-mac-packager/scripts

echo "Manage ENV"
export PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:$PATH

echo "Create dirs"
mkdir -p $LD
mkdir -p $BD
touch $LOG

echo "clean the build directories" 2>&1 | tee -a $LOG
# remove all dmg files older than X days
find $BD/*/*.dmg -mtime +5 -exec rm {} \;

echo "clean the log directories" 2>&1 | tee -a $LOG
# remove all files older than 60 days
find $LD/* -mtime +60 -exec rm {} \;


echo "Check GIT repo" 2>&1 | tee -a $LOG
cd $DIR/qgis-mac-packager
git fetch origin | tee -a $LOG
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse origin)

if [ $LOCAL = $REMOTE ]; then
    echo "GIT Up-to-date" 2>&1 | tee -a $LOG

    exit_status_ltr=0
    exit_status_pr=0
else
    echo "update qgis-mac-packager" 2>&1 | tee -a $LOG
    git rebase origin/master 2>&1 | tee -a $LOG

    echo "rebuild LTR" 2>&1 | tee -a $LOG
    $SD/run_ltr.bash 2>&1 | tee -a $LOG
    exit_status_ltr=$?

    echo "rebuild PR"
    $SD/run_pr.bash 2>&1 | tee -a $LOG
    exit_status_pr=$?
fi

echo "always build NIGHTLY"
$SD/run_nightly.bash 2>&1 | tee -a $LOG
exit_status_nightly=$?

if [ $exit_status_ltr -eq 0 -a $exit_status_pr -eq 0 -a $exit_status_nightly -eq 0 ]; then
    echo "SUCCESS" 2>&1 | tee -a $LOG
else
    echo "FAIL" 2>&1 | tee -a $LOG
    echo "Your nighly QGIS MacOS Build failed" | mail -s "MacOS Build Failure" info@lutraconsulting.co.uk -A $LOG
fi
exit $exit_status