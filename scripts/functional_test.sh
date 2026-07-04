#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

if [ -z "$TEST_FIREWALL" ] || [ -z "$TEST_API_CREDS" ]
then
  echo "ERROR: TEST_FIREWALL and TEST_API_CREDS have to be provided!"
  exit 1
fi

python3 -m pytest -c pytest_functional.ini $@
