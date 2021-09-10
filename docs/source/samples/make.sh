#!/bin/bash
set -euxo pipefail
# generate sample outputs and include directives for rst

ROOT="$(pwd)"
REPO_ROOT="${ROOT}/../../.."
BASE_URI_PATH="${REPO_ROOT}/tests/data/comparable"
DOCS_SOURCE_path="${REPO_ROOT}/docs/source}"
SAMPLE_OUTPUT_PATH="${REPO_ROOT}/docs/source/samples/output"

readarray -t commands_arr < commands.txt
readarray -t outfile_names_arr < <(cat commands.txt | tr -d '-' | sed 's/ /_/g' | sed -E 's/$/.out/g')
cd "${BASE_URI_PATH}"
for index in ${!commands_arr[*]}; do
  script -q -c "${commands_arr[$index]}" "${SAMPLE_OUTPUT_PATH}/${outfile_names_arr[$index]}"
done
exit

# cd "${DOCS_SOURCE_PATH}"
# find samples/output -name '*.out' | sed -E 's/^/.. literalinclude:: /g'
