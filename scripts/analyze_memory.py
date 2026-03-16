import json
import sys

GROWTH_AMOUNT_THRESHOLD = 10_000  # Import grows by 10KB
GROWTH_PERCENT_THRESHOLD = 0.5  # Import grows by 50%

SMALL_BOARD_THRESHOLD = 24_000  # 75% of small board memory

results_filepath = sys.argv[1]
original_results_filepath = sys.argv[2]

with open(results_filepath) as jsonfile:
    results: dict[str, int | None] = json.load(jsonfile)

with open(original_results_filepath) as jsonfile:
    original_results: dict[str, int | None] = json.load(jsonfile)

current_imports = set(results.keys())
original_imports = set(original_results.keys())

shared_imports = current_imports.intersection(original_imports)
new_imports = current_imports - original_imports
removed_imports = original_imports - current_imports

results_diffs: dict[str, tuple[int, int] | None] = {}

# Calculate differences for shared imports
for import_name in shared_imports:
    current_size = results[import_name]
    original_size = original_results[import_name]

    if None in (current_size, original_size):
        print(f"Cannot calculate growth for {import_name}")
        results_diffs[import_name] = None
        continue

    size_diff = current_size - original_size
    size_growth = size_diff / original_size

    results_diffs[import_name] = (size_diff, size_growth)

# Include newly added imports
for import_name in new_imports:
    current_size = results[import_name]

    if current_size is None:
        print(f"Cannot calculate growth for {import_name}")
        results_diffs[import_name] = None
        continue

    results_diffs[import_name] = (current_size, 0)

import pprint as pp

pp.pp(results_diffs)

# TODO: Check limits, add comments if over
