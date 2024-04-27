import argparse

# Define possible arguments:
parser = argparse.ArgumentParser(description="Parse performance files")

parser.add_argument('--file', help="Input file", default=None)
parser.add_argument('--folder', help="Input folder", default=None)

# Parse arguments:
args = parser.parse_args()

filePath: str = args.file
folderPath: str = args.folder
