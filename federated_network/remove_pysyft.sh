#!/bin/sh

set -a; source ~/.hagrid/PySyft/packages/grid/default.env; set +a

poetry run hagrid land $1 --force --silent
poetry run hagrid land $1 --force --prune-vol --silent

rm -rf ~/.hagrid
