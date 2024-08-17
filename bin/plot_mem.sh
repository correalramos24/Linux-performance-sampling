#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 ${SCRIPT_DIR}/../memory-sampling/plot_app/plot_mem.py $@