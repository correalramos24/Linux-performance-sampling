
from pathlib import Path
import pandas as pd
import re

def parse_pidstat_file(fPath: Path):
    

    with open(fPath, mode="r") as pidstat_file:
        columns = ['Timestamp', 'UID', 'PID', '%usr', '%system', '%guest', '%wait', '%CPU', 'CPU', 'Command']
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

        df[['%usr', '%system', '%guest', '%wait', '%CPU']] = df[['%usr', '%system', '%guest', '%wait', '%CPU']].astype(float)
        df[['Timestamp', 'UID', 'PID', 'CPU']] = df[['Timestamp', 'UID', 'PID', 'CPU']].astype(int)

        return num_cpus, df