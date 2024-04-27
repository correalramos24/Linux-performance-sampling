from arguments import *
from parsers import *
from plot import *

def main():
    results_df = None

    #1. One execution
    if filePath is not None:
        results_df = parse_perf_file(filePath)
        
        
    #2. Multi-results
    elif filesPath is not None:
        results_df = parse_perf_files(filesPath, dropAllNan=dropNaN)
        
    else:
        print("Either specify folder or a file")

    # PLOT, STDOUT or CSV
    if plot:
        plot_results(results_df)
    elif csv is not None:
        results_df.to_csv(csv)
    else:
        print(results_df)


if __name__ == "__main__":
    main()