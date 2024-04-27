#!/bin/bash

# Usage: 

SAMPLING_TIME=2
MEM_FILE="${HOSTNAME}-mem.log"

echo "Enable mem tracing with sampling every $SAMPLING_TIME"

free -s $SAMPLING_TIME &> $MEM_FILE &
PID_FREE=$!

$*

echo "Stop memory tracing. Results @ $MEM_FILE (units in KiB)"
kill $PID_FREE
