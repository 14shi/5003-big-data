#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

"$PYTHON_BIN" -m py_compile spark/jobs/batch_etl.py
"$PYTHON_BIN" -m py_compile streaming/streaming_job.py
"$PYTHON_BIN" -m py_compile kafka/producer.py
"$PYTHON_BIN" -m py_compile scripts/download_data.py

echo "Python syntax checks passed with $PYTHON_BIN."
