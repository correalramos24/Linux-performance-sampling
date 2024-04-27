
# OS performance sampling

Repository to gather utilities for gather performance indicators from 
the OS statistics and generate plots offline for performance analysis.

## Performance metrics
Use perf for gather performance metrics, from the OS. A bash wrapper is used 
for simplicity. After the execution the output file can be parsed with a Python
plotting app. The are several use cases for this:

1. Parse 1 performance file and 
2. Compare N performance files [WIP]
3. Plot N performance files results [WIP]
4. Check balance ofr N performance files of an multi-node execution (MPI) [WIP]

## Memory sampling

> TODO: memory-profiling reference

## I/O performance sampling

To sample the I/O performance of an application, use:

````bash
SAMP_INTERVAL=10

pidstat -d -h --dec=0 $SAMP_INTERVAL 
# Discard header:
pidstat -d -h --dec=0 $SAMP_INTERVAL   | grep -v '^# Time' &> io_sampling.log
````

