
import pandas as pd
import numpy as np
from pathlib import Path

cols_mem = ["timing","total","used","free","shared","buff/cache","available"]
cols_swp = ["total_swap", "used_swap", "free_swap"]

def parse_mem_file(fPath : Path, swap: bool = False, samp_time: int = 1,
                   file_pattern="-mem.log") -> pd.DataFrame :

    """Parser for a file from free command.
    Args:
        fPath (str): _description_
        swap (bool, optional): Parse swap also. Defaults to False.
        file_pattern (str, optional): File name pattern for the hostname. 
            Defaults to "-mem.log".

    Returns:
        MemoryResults: all the information from the fPath file.
    """

    data = []
    timing = 0
    # 1. Parse the file and accum data:
    with open(fPath, mode='r') as mem_file:
        for line in mem_file.readlines():
            if "Mem: " in line:
                data.append([timing] + line.split()[1:])
                timing+=samp_time
            if swap and "Swap: " in line:
                data[-1].extend(line.split()[1:])
            
    # 2. Build dataframe:
    cols = cols_mem if not swap else cols_mem + cols_swp
    df = pd.DataFrame(columns=cols, data=data).astype(int)
    df["timing"] = df["timing"].astype(str)
    
    return df

