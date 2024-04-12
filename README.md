
# OS performance sampling

Repository to gather utilities for gather performance indicators from 
the OS statistics and generate plots offline for performance analysis.

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

