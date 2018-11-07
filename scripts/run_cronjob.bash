#!/usr/bin/env bash

export QGIS_CRONJOB=1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
$DIR/run_nightly.bash
