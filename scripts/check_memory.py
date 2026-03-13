import json
import sys

import circuitpy_sim

import_name = sys.argv[1]

simulator = circuitpy_sim.Simualtor()

result = simulator.simulate()
result_json = json.dumps(result)

with open(import_name + ".json", mode="w") as jsonfile:
    jsonfile.write(result)

print(f"Import size of {import_name}: {result}")
