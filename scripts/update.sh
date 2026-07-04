#!/usr/bin/env bash

if [ -z "$1" ]
then
  VERSION='latest'
else
  VERSION="$1"
fi

set -euo pipefail

cd "$(dirname "$0")/.."
BASE="$(pwd)"

rm -rf build/
mkdir -p build
cd build
git clone https://github.com/O-X-L/ansible-opnsense
cd ansible-opnsense
git checkout "$VERSION"

cd "$BASE"
rm -r "${BASE}/src/oxl_opnsense_client/plugins/"*
cp -r "${BASE}/build/ansible-opnsense/plugins/"* "${BASE}/src/oxl_opnsense_client/plugins/"

find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec touch {}/__init__.py \;
find "${BASE}/src/oxl_opnsense_client/plugins/" -type d -exec git add {}/*.py \;

function patch() {
  file="$1"

  echo "PATCH: ${file}"
  sed -i 's|^from ansible.module_utils.basic|from basic.ansible|g' "$file"
  # sed -i 's|^from ansible.module_utils.common.arg_spec|from basic.ansible|g' "$file"
  sed -i 's|from ansible_collections.oxlorg.opnsense.plugins|from plugins|g' "$file"
  sed -i "s|'ansible_collections.oxlorg.opnsense.plugins|'plugins|g" "$file"
  if echo "$file" | grep -q 'plugins/modules/'
  then
    sed -i 's|def run_module():|def run_module(module_input):|g' "$file"
    sed -i 's|module = AnsibleModule(|module = AnsibleModule(\n        module_input=module_input,|g' "$file"
    sed -i 's|    AnsibleModule(|    AnsibleModule(\n        module_input=module_input,|g' "$file"
    sed -i 's|module.exit_json(\*\*result)|return result|g' "$file"
    sed -i 's|module.exit_json(data=info)|return info|g' "$file"
    sed -i 's|def main():||g' "$file"
    sed -i 's|^    run_module()||g' "$file"
    sed -i 's|^    main()|    pass|g' "$file"
  fi
}
export -f patch

find "${BASE}/src/oxl_opnsense_client/plugins/" -type f -name '*.py' ! -name '_*' -exec bash -c 'patch "$0"' {} \;

sed -i 's|def diff_remove_empty(diff: dict, to_none: bool = False|def diff_remove_empty(diff: dict, to_none: bool = True|g' "${BASE}/src/oxl_opnsense_client/plugins/module_utils/helper/main.py"

echo ''
bash scripts/lint.sh

echo ''
bash scripts/unit_test.sh
