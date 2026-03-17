# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

import shutil
import tomllib
import os

# Open the repository's pyproject.toml
with open("pyproject.toml", mode="rb") as tomlfile:
    pyproject = tomllib.load(tomlfile)

# Get the setuptools table
setuptools = pyproject["tool"]["setuptools"]

# Get the intended CIRCUITPY filepath
circuitpy_folder = os.path.join(os.getcwd(), "CIRCUITPY")

# Get the library and copy to drive depending on if its a library of package
if "py-modules" in setuptools:
    library_file = setuptools["py-modules"][0] + ".py"
    shutil.copy(library_file, circuitpy_folder)
elif "packages" in setuptools:
    library_folder = setuptools["packages"][0]
    drive_folder = os.path.join(circuitpy_folder, library_folder)
    os.mkdir(drive_folder)
    shutil.copytree(library_folder, drive_folder, dirs_exist_ok=True)
else:
    raise KeyError("Neither modules nor packages are defined in pyproject.toml")
