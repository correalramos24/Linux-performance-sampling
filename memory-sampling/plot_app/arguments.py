
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Memory sampling script")

# INPUTS
parser.add_argument('--input', required=True, 
                    help="Input file(s), can use wildcard like *", nargs="+")
parser.add_argument('--samp',
                    help='Sampling time of the input file(s)', default=1)
# SAVE NAME:
parser.add_argument('--save', default=None, 
                    help="Enable and define save file name")
# PLOT OPTIONS:
parser.add_argument('--swap', action='store_true', help="Enable swap plotting")
parser.add_argument('--total', action='store_true', 
                    help="Enable total memory available?")
parser.add_argument('--percentage', action='store_true', 
                    help="Plot perc of usage")
parser.add_argument('--legend', action='store_true', 
                    help="Plot legend")
parser.add_argument('--output_units', default="KiB",
                    help="Set output units for the plots")
#parser.add_argument('--output_scale', default=1, 
#                    help="Factor that will be divide the memory results")
app_args = parser.parse_args()

files  : list[Path] = app_args.input
sampl  : int  = int(app_args.samp)

swap   : bool = app_args.swap
total  : bool = app_args.total
percnt : bool = app_args.percentage

legend : bool = app_args.legend
save   : str  = app_args.save

unit_o : str  = app_args.output_units
#unit_s : int  = int(app_args.output_scale)

f_pat  : str  = "-mem.log"

if files is None:
    print("Error: No input files specified")
    exit(1)
print("Sampling time set to", sampl)
print("Units set to", unit_o)