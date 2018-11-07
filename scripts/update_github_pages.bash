#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

python3 $DIR/../qgis-mac-packager/get_computer_info.py > $DIR/../docs/README.md
