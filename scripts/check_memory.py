# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

import json
import sys

import circuitpy_sim

# Get command line arguments
firmware_filepath = sys.argv[1]
flash_filepath = sys.argv[2]
circuitpy_filepath = sys.argv[3]
import_names: list[str] = json.loads(sys.argv[4])
results_filepath = sys.argv[5]

results = {}
for import_name in import_names:
    # Create code.py
    code_text = (
        "import gc\n"
        "pre = gc.mem_free()\n"
        f"import {import_name}\n"
        "post = gc.mem_free()\n"
        "used = pre - post\n"
        "print(used)"
    )
    with open("CIRCUITPY/code.py", mode="w") as code_fp:
        code_fp.write(code_text)

    # Prepare the flash and simulate CircuitPython
    circuitpy_sim.prepare_flash(flash_filepath, circuitpy_filepath)
    result = circuitpy_sim.simulate(firmware_filepath, flash_filepath)

    # Attempt to parse the number (or handle errors)
    try:
        result_parsed = int(result)
    except ValueError:
        print(f"Could not parse result of {import_name}, received:", result)
        result_parsed = None

    # Store the result (and also print it for convenience)
    results[import_name] = result_parsed
    print(f"Import size of {import_name}: {result}")

# WRite the overall results to disk
with open(results_filepath, mode="w") as jsonfile:
    json.dump(results, jsonfile)
