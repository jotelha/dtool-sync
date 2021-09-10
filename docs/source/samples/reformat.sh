#!/bin/bash
set -euxo pipefail
# generate sample outputs and include directives for rst

ROOT="$(pwd)"
REPO_ROOT="${ROOT}/../../.."
BASE_URI_PATH="${REPO_ROOT}/tests/data/comparable"
DOCS_SOURCE_path="${REPO_ROOT}/docs/source}"
SAMPLE_OUTPUT_PATH="${REPO_ROOT}/docs/source/samples/output"

for infile in ${SAMPLE_OUTPUT_PATH}/*.out; do
    # remove 'script' command header and footer and replace system-specific paths with generic
    tmpfile=$(mktemp)
    cat "${infile}" \
        | sed -E 's|file://.*/tests/data/comparable|file://path/to|g' \
        | sed '/^Script started/d' | sed '/^Script done/d' > "${tmpfile}"
    cat "${tmpfile}" > "${infile}"
    rm -f "${tmpfile}"
done
exit
