# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

import json
import os
import pathlib
import tomllib

# Open the repository's pyproject.toml
with open("pyproject.toml", mode="rb") as tomlfile:
    pyproject = tomllib.load(tomlfile)

# Get the setuptools table
setuptools = pyproject["tool"]["setuptools"]

# Get the intended CIRCUITPY filepath
circuitpy_folder = os.path.join(os.getcwd(), "CIRCUITPY")

# Get the filepaths for the library
if "py-modules" in setuptools:
    filepaths = [setuptools["py-modules"][0] + ".py"]
elif "packages" in setuptools:
    filepaths = [name.replace(".", "/") for name in setuptools["packages"]]
else:
    raise KeyError("Neither modules nor packages are defined in pyproject.toml")

# Convert the filepaths into Path objects
paths = [pathlib.Path(filepath) for filepath in filepaths]

# Gather the intended files
import_paths: set[pathlib.Path] = set()
for path in paths:
    import_paths.add(path)
    if path.is_dir():
        for matching_file in path.glob("**/*.py"):
            matching_name = (
                matching_file.parent
                if matching_file.name in ("__init__.py", "__main__.py")
                else matching_file
            )
            import_paths.add(matching_name)

# Convert paths to import names
import_names = set()
for path in import_paths:
    if not path.is_file() and not (path / "__init__.py").is_file():
        continue
    path_like = str(path).replace("/", ".")
    if path_like.endswith(".py"):
        path_like = path_like[:-3]
    import_names.add(path_like)

# Write the imports to the console as a JSON string
imports_json = json.dumps(list(import_names))
print(imports_json)
