import shutil
import tomllib
import os
import pathlib

with open("pyproject.toml", mode="rb") as tomlfile:
    pyproject = tomllib.load(tomlfile)

setuptools = pyproject["tool"]["setuptools"]

circuitpy_folder = os.path.join(os.getcwd(), "CIRCUITPY")

pathlib.Path(circuitpy_folder).mkdir()

if "py-modules" in setuptools:
    library_file = setuptools["py-modules"][0] + ".py"
    shutil.copy(library_file, circuitpy_folder)
elif "packages" in setuptools:
    library_folder = setuptools["packages"][0]
    shutil.copytree(library_folder, circuitpy_folder, dirs_exist_ok=True)
else:
    raise KeyError("Neither modules nor packages are defined in pyproject.toml")
