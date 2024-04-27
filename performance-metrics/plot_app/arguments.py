import argparse

# Define possible arguments:
parser = argparse.ArgumentParser(description="Parse performance files")

# INPUTS
parser.add_argument('--file', 
                    help="Input file", 
                    default=None)
parser.add_argument('--files', 
                    help="Input files, can use bash wildcard like *", nargs="+")

# OUTPUTS
parser.add_argument("--plot",
                    help="Enable plotting",
                    action='store_true')
parser.add_argument('--csv', 
                    help="Enable CSV output",
                    default=None)
#OPTIONS
parser.add_argument('--dropnan',
                    help="Drop counter if all values are NaN", 
                    action='store_true')

# Parse arguments:
args = parser.parse_args()

filePath: str = args.file
filesPath: list[str] = args.files
dropNaN : bool = args.dropnan
plot : bool = args.plot
csv : str = args.csv