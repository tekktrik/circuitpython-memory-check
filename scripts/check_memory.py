import json
import sys

import circuitpy_sim

firmware_filepath = sys.argv[1]
flash_filepath = sys.argv[2]
circuitpy_filepath = sys.argv[3]
import_names: list[str] = json.loads(sys.argv[4])
results_filepath = sys.argv[5]

results = {}
for import_name in import_names:
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

    circuitpy_sim.prepare_flash(flash_filepath, circuitpy_filepath)
    result = circuitpy_sim.simulate(firmware_filepath, flash_filepath)

    try:
        result_parsed = int(result)
    except ValueError:
        print(f"Could not parse result of {import_name}, received:", result)
        continue

    results[import_name] = result_parsed

    print(f"Import size of {import_name}: {result}")

with open(results_filepath, mode="w") as jsonfile:
    json.dump(results, jsonfile)
