import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Pidstat file parser and plotter")

#INPUT
parser.add_argument('files', nargs='+', help="Input files", type=Path)
parser.add_argument('--mode', choices=["cpu", "io"], default="cpu")

#PARSE DATA:
parser.add_argument('--drop', 
                    type=float, default=None, 
                    help="Drop pid records with less than X perc. of CPU usage")

# SAVE DATA:
parser.add_argument('--save-csv', help="Save csv for each parsed file?", 
                    action='store_true')
parser.add_argument('--save-plot', help="Save plot with name")

# MISC:
parser.add_argument('--split-plots', 
                    help="Get one plot for each app name listed here", 
                    nargs="+")
#parser.add_argument('--absolute-ts', 
#                    action='store_true', help="Use absolute timing")

# Parse arguments:
args = parser.parse_args()

files : list[Path]  = args.files
#rel_ts: bool        = not(args.absolute_ts)
rel_ts: bool        = True
mode  : str         = args.mode
drop  : float       = args.drop
save_csv: bool      = args.save_csv
save_plot:str       = args.save_plot
split_plot:list[str]= args.split_plots

if drop is not None:
    print("Dropping PIDs with less %CPU than", drop, "for all the pidstat file")
    print("Drooping PIDs with more than 50% NaN values for %CPU!")

if split_plot is not None:
    print(f"Requested {len(split_plot)}, plots. One for each app")
    print("\n".join(split_plot))