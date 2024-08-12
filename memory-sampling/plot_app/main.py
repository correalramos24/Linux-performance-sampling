#!/bin/python3

from arguments import *
from parsing import *
from plot import *
import pandas as pd

def main():

    results : list[pd.DataFrame] = []
    hostnames : list[str] = []
    
    # 1. Parse input files:
    for file in files:
        try:
            file = Path(file)
            hostnames.append(file.name.split(f_pat)[0])
            print(f"Parsing {file} file from host {hostnames[-1]} ...")
            data = parse_mem_file(file, swap)
            
            # Compute the percentage, scale units, if required!
            if len(data) > 0 and (percnt or unit_s != 1):
                if unit_s != 1 and not percnt:
                    data = scale_data(data, swap, unit_s)
                if percnt:
                    data = compute_percnt(data, unit_s)
            # Append data to plot later
            results.append(data)

        except Exception as e:
            print(f"Can't parse {file} file, skipping")
            print(e)
        finally:
            print(f"DONE! {file}")
    
    # 2. Check if there are results to plot:
    if len(results) == 0:
        print("Unable to find any memory information, check input files!")
        exit(1)

    # 3. Generate plot
    plot_plt_mem_perc(results, hostnames, swap, unit_o, percnt, total, legend, save)
    #plot_plt_memory_results(results, sampl, plot_format, 
                            #legend,total, save, unit_s, unit_o)


if __name__ == "__main__":
    main()
