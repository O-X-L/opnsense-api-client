#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."
BASE="$(pwd)"

rm -rf build/
mkdir -p build
cd build
git clone https://github.com/O-X-L/ansible-opnsense

cd "$BASE"
rm -r "${BASE}/src/oxl_opnsense_client/plugins/"*
cp -r "${BASE}/build/ansible-opnsense/plugins/"* "${BASE}/src/oxl_opnsense_client/plugins/"

find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec touch {}/__init__.py \;
find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec git add {}/*.py \;

files="$(find "${BASE}/src/oxl_opnsense_client/plugins/" -type f -name '*.py' ! -name '_*')"
