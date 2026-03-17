# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

import json
import sys

from collections import namedtuple

GROWTH_AMOUNT_THRESHOLD = 10_000  # Import grows by 10KB
GROWTH_PERCENT_THRESHOLD = 0.5  # Import grows by 50%
SMALL_BOARD_THRESHOLD = 24_000  # 75% of small board memory

# Keep track of import information in namedtuple
ImportStats = namedtuple(
    "ImportStats", ["original_size", "current_size", "diff", "growth_percent"]
)

# Get command line arguments
results_filepath = sys.argv[1]
original_results_filepath = sys.argv[2]
analysis_filepath = sys.argv[3]

# Get new results
with open(results_filepath) as jsonfile:
    results: dict[str, int | None] = json.load(jsonfile)

# Get previous results
with open(original_results_filepath) as jsonfile:
    original_results: dict[str, int | None] = json.load(jsonfile)

# Get imports
current_imports = set(results.keys())
original_imports = set(original_results.keys())

# Determine Venn diagram of imports
shared_imports = current_imports.intersection(original_imports)
new_imports = current_imports - original_imports
removed_imports = original_imports - current_imports

# Keep track of import status
ignored_imports: list[str] = []
changed_import_sizes: dict[str, ImportStats] = {}
added_import_sizes: dict[str, int] = {}
unchanged_import_sizes: dict[str, int] = {}

# Calculate differences for shared imports
for import_name in shared_imports:
    current_size = results[import_name]
    original_size = original_results[import_name]

    # Ignore changes where
    if current_size is None and original_size is None:
        print(f"Cannot calculate new or previous import size for {import_name}")
        ignored_imports.append(import_name)
        continue
    elif current_size is None:
        print(f"Cannot calculate new import size for {import_name}")
        ignored_imports.append(import_name)
        continue
    elif original_size is None:
        print(f"Cannot calculate previous import size for {import_name}")
        changed_import_sizes[import_name] = ImportStats("?", current_size, "X", "X")
        continue

    # Ignore if no changes were made
    if current_size == original_size:
        print(f"No change in import size for {import_name}")
        unchanged_import_sizes[import_name] = current_size
        continue

    # Calculate size differencs
    size_diff = current_size - original_size
    size_growth = size_diff / original_size

    # Warning thresholds currently not used
    # size_triggered = current_size >= SMALL_BOARD_THRESHOLD
    # diff_triggered = size_diff >= GROWTH_AMOUNT_THRESHOLD
    # mult_triggered = size_growth >= GROWTH_PERCENT_THRESHOLD

    # Record changes
    changed_import_sizes[import_name] = ImportStats(
        original_size, current_size, size_diff, size_growth
    )

# Include newly added imports
for import_name in new_imports:
    current_size = results[import_name]

    # Ignore imports that cannot be calculated currently
    if current_size is None:
        print(f"Cannot calculate growth for {import_name}")
        ignored_imports.append(import_name)
        continue

    # Record changes
    added_import_sizes[import_name] = current_size

# Create text for additions
added_text = ""
if added_import_sizes:
    added_text = "The following imports were added:\n\n"
    for import_name, import_size in sorted(
        added_import_sizes.items(), key=lambda item: item[0]
    ):
        added_text += f"- {import_name}: {import_size} bytes\n"
    added_text += "\n"

# Create text for changes
changed_text = ""
if changed_import_sizes:
    changed_text = "The following imports were changed:\n\n"
    for import_name, import_stats in sorted(
        changed_import_sizes.items(), key=lambda item: item[0]
    ):
        changed_text += f"- {import_name}: {import_stats.original_size} -> {import_stats.current_size} bytes ({import_stats.diff} bytes, {round(import_stats.growth_percent * 100, 2)}% growth)\n"
    changed_text += "\n"

# Create text for unchanged
unchanged_text = ""
if unchanged_import_sizes:
    unchanged_text = "The following imports stayed the same:\n\n"
    for import_name, import_size in sorted(
        unchanged_import_sizes.items(), key=lambda item: item[0]
    ):
        unchanged_text += f"- {import_name}: {import_size} bytes\n"
    unchanged_text += "\n"

# Create text for ignored
ignored_text = ""
if ignored_imports:
    ignored_text = "The following imports could not be measured and were ignored (see workflow and artifacts):\n\n"
    for import_name in sorted(ignored_imports):
        ignored_text += f"- {import_name}\n"
    ignored_text += "\n"

# Compile texts and write to disk
analysis_text = added_text + changed_text + unchanged_text + ignored_text
with open(analysis_filepath, mode="w") as analysis_file:
    analysis_file.write(analysis_text)
