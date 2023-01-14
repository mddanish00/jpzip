# jpzip is a simple program to extract archive that contains files with
# name in Japanese correctly using 7zip.
#
# Copyright (C) 2022 Miracutor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
import subprocess
import sys
from pathlib import Path

# Check if 7za.exe is in 7z folder in the same directory as this script
exe_7zip = Path(sys.executable).parent / Path("7z", "7za.exe")
if not exe_7zip.exists():
    print(
        "7za.exe not found in 7z folder. Please download 7za.exe from https://www.7-zip.org/download.html"
    )
    exit()

# The jpzip program information
parser = argparse.ArgumentParser(
    description="jpzip is a simple program to extract archive that contains files with "
    "name in Japanese correctly using 7zip. jpzip v1.0.2"
)

# The jpzip program version info
parser.add_argument("-v", "--version", action="version", version="v1.0.2")

# The jpzip program arguments
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-o",
    "--output",
    help="Output directory. If not specified, output will be at the same directory "
    "as the archive.",
)
group.add_argument(
    "-os",
    "--output_same",
    action="store_true",
    help="Output to a new directory with same name as the archive name.",
)
parser.add_argument("input", help="Input archive.")

#
args = parser.parse_args()

# Check if the input archive exists
input_zip: Path = Path(args.input)
if not input_zip.exists():
    print(f"The input archive, {input_zip} does not exist.")
    exit()

if args.output_same:
    # Create a new folder with the same name as the archive
    output_dir = input_zip.parent / Path(input_zip.stem)
    # check if the output directory already exists
    if output_dir.exists() is False:
        output_dir.mkdir()
elif args.output:
    output_dir = Path(args.output)
    # check if the output directory already exists
    if output_dir.exists() is False:
        output_dir.mkdir(parents=True)
else:
    # Output to the same directory as the archive
    output_dir = input_zip.parent

args_exe = [
    str(exe_7zip.resolve()),
    "x",
    "-mcp=932",
    str(input_zip.resolve()),
    "-o" + str(output_dir.resolve()),
]

# Run 7zip with the arguments
subprocess.run(args_exe)
