import shutil
import tomllib
import os
import pathlib

with open("pyproject.toml", mode="rb") as tomlfile:
    pyproject = tomllib.load(tomlfile)

setuptools = pyproject["tool"]["setuptools"]

circuitpy_folder = os.path.join(os.getcwd(), "CIRCUITPY")

if "py-modules" in setuptools:
    library_file = setuptools["py-modules"][0] + ".py"
    os.path.join(circuitpy_folder, library_file)
    os.remove(library_file)
elif "packages" in setuptools:
    library_folder = setuptools["packages"][0]
    drive_folder = os.path.join(circuitpy_folder, library_folder)
    os.rmdir(drive_folder)
else:
    raise KeyError("Neither modules nor packages are defined in pyproject.toml")
