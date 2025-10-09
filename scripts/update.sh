#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."
BASE="$(pwd)"

#rm -rf build/
#mkdir -p build
#cd build
#git clone https://github.com/O-X-L/ansible-opnsense

cd "$BASE"
rm -r "${BASE}/src/oxl_opnsense_client/plugins/"*
cp -r "${BASE}/build/ansible-opnsense/plugins/"* "${BASE}/src/oxl_opnsense_client/plugins/"

find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec touch {}/__init__.py \;
find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec git add {}/*.py \;

function patch() {
  file="$1"

  echo "PATCH: ${file}"
  sed -i 's|^from ansible.module_utils.basic|from basic.ansible|g' "$file"
  sed -i 's|^from ansible.module_utils.common.arg_spec|from basic.ansible|g' "$file"
  sed -i 's|from ansible_collections.oxlorg.opnsense.plugins|from plugins|g' "$file"
}
export -f patch

find "${BASE}/src/oxl_opnsense_client/plugins/" -type f -name '*.py' ! -name '_*' -exec bash -c 'patch "$0"' {} \;

echo ''
bash scripts/lint.sh

echo ''
bash scripts/unit_test.sh
