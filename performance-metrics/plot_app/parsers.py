
import pandas as pd
import numpy as np

# FORMAT:
# 1. # for comments
# 2. <not counted> for no data for that metric
# 3. empty str ('') for no units

NULL_DATA_STR="<not counted>"
IPC_STR="insn per cycle\n"
CPU_STR="CPUs utilized\n"

def parse_perf_file(fPath: str, SEP: str  = ',', dropAllNan: bool = False):
    # 1. Parse file
    info = parser_file(fPath, SEP)
    # 2. Generate dataframe with the data:
    df = pd.DataFrame(data=info,index=[fPath])
    df.fillna(np.nan, inplace=True)
    if dropAllNan: df = df.dropna(axis=1, how='all')
    return df 

def parse_perf_files(fPaths: str, SEP: str  = ',', dropAllNan: bool = False) -> pd.DataFrame:
    data = []

    for fPath in fPaths:
        # Parse i-th file && append data
        data.append(parser_file(fPath, SEP))


    # CREAE & RETURN PANDAS DATAFRAME
    df = pd.DataFrame(data=data,index=fPaths)
    df.fillna(np.nan, inplace=True)
    if dropAllNan: df = df.dropna(axis=1, how='all')
    return df


def parser_file(fPath: str, SEP: str  = ',') -> dict:
    ret = {}
    with open(fPath, mode='rt') as perf_file:
        for line in perf_file.readlines():
            if '#' not in line:
                info = line.split(SEP)
                # Line with data ?
                if len(info) > 1:
                    value, unit, metric = info[0:3]
                    # Data?
                    if value != NULL_DATA_STR:
                        if unit == '':
                            ret[metric] = int(value)
                        else:
                            ret[metric+ ' (' + unit + ')'] = float(value)
                    else:
                        ret[metric] = None

                    # IPC or CPUs used?
                    if CPU_STR in info:
                        ret[CPU_STR.strip()] = float(info[info.index(CPU_STR)-1])
                    if IPC_STR in info:
                        ret[IPC_STR.strip()] = float(info[info.index(IPC_STR)-1])
                    
        return ret