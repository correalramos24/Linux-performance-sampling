
from pathlib import Path
import pandas as pd
import re

def parse_pidstat_file(fPath: Path, mode="cpu", target_app="ifsMASTER.SP"):
    

    with open(fPath, mode="r") as pidstat_file:
        columns_cpu = ['Timestamp', 'UID', 'PID', '%usr', '%system', '%guest', '%wait', '%CPU', 'CPU', 'Command']
        columns_io  = ['Timestamp', 'UID','PID', "kB_rd/s", 'kB_wr/s', 'kB_ccwr/s', 'iodelay', 'Command']
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

        return num_cpus, df
