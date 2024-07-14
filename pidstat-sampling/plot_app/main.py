import sys
from pathlib import Path
from parsers import *
from plot import *

USE_REALTIVE_TS=True

def main():

    #Argument parsing:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pidstat-log-file>")
        sys.exit(1)
    
    # Parse file:
    pidstat_file = Path(sys.argv[1])
    print(f"Parsing {pidstat_file}...", end="")
    num_cpus, df = parse_pidstat_file(pidstat_file)
    print(f"Completed! Found {len(df)} records for {num_cpus} CPU!")

    # Convert timestamp to human-readable:
    if USE_REALTIVE_TS:
        min_timestamp = df['Timestamp'].min()
        df['Timestamp'] = df['Timestamp'] - min_timestamp
    else:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    
    #print(df)

    plot_pidstat(num_cpus, df)


if __name__ == "__main__":
    main()