import json
import sys

import circuitpy_sim

firmware_filepath = sys.argv[1]
flash_filepath = sys.argv[2]
import_name = sys.argv[3]

result = circuitpy_sim.Simualtor.simulate(firmware_filepath, flash_filepath)
result_json = json.dumps(result)

with open(import_name + ".json", mode="w") as jsonfile:
    jsonfile.write(result)

print(f"Import size of {import_name}: {result}")
