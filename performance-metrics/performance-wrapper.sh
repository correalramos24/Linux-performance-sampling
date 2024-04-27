#!/bin/bash

# Usage: 
# To custom the event to record, use perf list

OUT_FILE=${HOSTNAME}.perf>A

perf stat \
    -e duration_time,user_time,system_time,instructions,cycles,task-clock \
    --metric-no-merge \
    -o ${OUT_FILE}  -x ,\
    $*