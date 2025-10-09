#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo ''
echo 'LINTING Python'
echo ''

python3 -m pylint --recursive=y .

echo ''
echo 'FINISHED LINTING!'
echo ''
