
# FORMAT:
# 1. # for comments
# 2. <not counted> for no data for that metric
# 3. empty str ('') for no units

NULL_DATA_STR="<not counted>"
IPC_STR="insn per cycle\n"
CPU_STR="CPUs utilized\n"

def parse_perf_file(fPath: str, SEP: str  = ','):
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
                            ret[metric] = value
                        else:
                            ret[metric] = value + " " + unit
                    else:
                        ret[metric] = None

                    # IPC or CPUs used?
                    if CPU_STR in info:
                        ret[CPU_STR.strip()] = info[info.index(CPU_STR)-1]
                    if IPC_STR in info:
                        ret[IPC_STR.strip()] = info[info.index(IPC_STR)-1]
                    
        return ret