
from pathlib import Path
import pandas as pd
import re

columns_cpu = ['Timestamp', 'UID', 'PID', '%usr', '%system', '%guest', '%wait', '%CPU', 'CPU', 'Command']
columns_io  = ['Timestamp', 'UID','PID', "kB_rd/s", 'kB_wr/s', 'kB_ccwr/s', 'iodelay', 'Command']
#columns_mem

def parse_pidstat_file( fPath: Path, 
                        mode: str,
                        rel_ts: bool,
                        drop_min: float = None,
                        target_app="ifsMASTER.SP") -> tuple[int, pd.DataFrame]:

    with open(fPath, mode="r") as pidstat_file:
        
        if mode == "cpu":
            columns = columns_cpu
        if mode == "io":
            columns = columns_io
        num_cpus = None
        data = []

        for line in pidstat_file.readlines():
            # Get Number of CPUS
            if "CPU)" in line:
                pattern = r'\((\d+) CPU\)'
                match = re.search(pattern, line)
                num_cpus = int(match.group(1)) if match else None

                continue
            #Header or empty line!
            if line.strip() == '' or "PID" in line:
                continue
            # Found average => END
            if line.startswith("Average:"):
                break
            # Content line:
            line_info = line.split()
            data.append(line_info)
        
        df = pd.DataFrame(data, columns=columns)
        df_target_app = df[df['Command'] == target_app]
        df[['Timestamp', 'UID', 'PID']] = df[['Timestamp', 'UID', 'PID']].astype(int)

        if mode == "cpu":
            df[['%usr', '%system', '%guest', '%wait', '%CPU']] = df[['%usr', '%system', '%guest', '%wait', '%CPU']].astype(float)
            df[['Timestamp', 'UID', 'PID', 'CPU']] = df[['Timestamp', 'UID', 'PID', 'CPU']].astype(int)

            df = df[['Timestamp', 'PID', 'CPU', '%CPU', '%usr', '%system', 'Command']]
            
            print(f"Unique combinations of PID and CPU for {target_app}, {len(df_target_app[['PID', 'CPU']].drop_duplicates())}")
        if mode == "io":
            df[["kB_rd/s", 'kB_wr/s', 'kB_ccwr/s']] = df[["kB_rd/s", 'kB_wr/s', 'kB_ccwr/s']].astype(float)
            df[['iodelay']] = df[['iodelay']].astype(int)
        
        print(f"Unique {target_app} PIDs : {df_target_app['PID'].nunique()}")

        # Convert timestamp to human-readable:
        if rel_ts:
            min_timestamp = df['Timestamp'].min()
            df['Timestamp'] = df['Timestamp'] - min_timestamp
        else:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
            print("WARNING! Feature in development!")

        if drop_min is not None:
            print(drop_min, type(drop_min))
            orinal_size=len(df)
            # DROP PIDS that ! any >= 5% CPU usage
            ids_to_keep = df.groupby('PID').filter(lambda x: (x['%CPU'] >= drop_min).any())['PID'].unique()
            df = df[df['PID'].isin(ids_to_keep)]
            
            # DROP PIDs that more than /2 are NaN
            threshold = len(df.columns) / 3
            df = df.dropna(thresh=threshold)

            print(f"{orinal_size-len(df)} records dropped. From {orinal_size} to {len(df)}")

        return num_cpus, df
