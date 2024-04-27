from arguments import *
from parsers import *

def main():
    #1. csv for a one node execution
    if filePath is not None:
        info = parse_perf_file(filePath)
        for metric, value in info.items():
            print(metric, "=>", value)
    #2. csv for a multi-node execution
    elif folderPath is not None:
        pass    
    else:
        print("Either specify folder or a file")




if __name__ == "__main__":
    main()