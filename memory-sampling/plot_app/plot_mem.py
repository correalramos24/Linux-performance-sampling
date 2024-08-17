#!/gpfs/apps/MN5/GPP/PYTHON/3.12.1/INTEL/bin/python3
from arguments import *
from parsing import *
from plot import *
import pandas as pd

def main():

    results : list[pd.DataFrame] = []
    hostnames : list[str] = []
    err_files : int = 0

    # 1. Parse input files:
    print(f"Going to parse {len(files)} files...")
    for i, file in enumerate(files):
        try:
            file = Path(file)
            hostnames.append(file.name.split(f_pat)[0])
            #print(f"{i}\tParsing {file} file from host {hostnames[-1]} ...")
            print(i, end=" ")
            data = parse_mem_file(file, swap)
            
            # Compute the percentage, scale units, if required!
            if len(data) > 0 and (percnt or unit_s != 1):
                if unit_s != 1 and not percnt:
                    data = scale_data(data, unit_s)
                if percnt:
                    data = compute_percnt(data, swap)
            # Append data to plot later
            results.append(data)

        except Exception as e:
            print(f"Can't parse {file} file, skipping")
            print(e)
            err_files += 1
        #finally:
            #print(f"DONE! {file}")
    
    print(f"Parsing completed, found {err_files} erronoeus pidstat files")

    # 2. Check if there are results to plot:
    if len(results) == 0:
        print("Unable to find any memory information, check input files!")
        exit(1)

    # 3. Generate plot
    
    plot_plt_mem_perc(results, hostnames, swap, unit_o, percnt, total, legend, save, avail)
    #plot_plt_memory_results(results, sampl, plot_format, 
                            #legend,total, save, unit_s, unit_o)


if __name__ == "__main__":
    main()
