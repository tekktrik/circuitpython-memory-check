# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

import json
import sys

from collections import namedtuple

# UNKNOWN_MARKER = "unknown"
# LOST_MARKER = "lost"
# RETRACKED_MARKER = "retracked"

GROWTH_AMOUNT_THRESHOLD = 10_000  # Import grows by 10KB
GROWTH_PERCENT_THRESHOLD = 0.5  # Import grows by 50%

SMALL_BOARD_THRESHOLD = 24_000  # 75% of small board memory

ImportStats = namedtuple(
    "ImportStats", ["original_size", "current_size", "diff", "growth_percent"]
)

results_filepath = sys.argv[1]
original_results_filepath = sys.argv[2]
analysis_filepath = sys.argv[3]

with open(results_filepath) as jsonfile:
    results: dict[str, int | None] = json.load(jsonfile)

with open(original_results_filepath) as jsonfile:
    original_results: dict[str, int | None] = json.load(jsonfile)

current_imports = set(results.keys())
original_imports = set(original_results.keys())

shared_imports = current_imports.intersection(original_imports)
new_imports = current_imports - original_imports
removed_imports = original_imports - current_imports

# results_diffs: dict[str, ImportStats | str] = {}
ignored_imports: list[str] = []
changed_import_sizes: dict[str, ImportStats] = {}
added_import_sizes: dict[str, int] = {}

# Calculate differences for shared imports
for import_name in shared_imports:
    current_size = results[import_name]
    original_size = original_results[import_name]

    if current_size is None and original_size is None:
        print(f"Cannot calculate new or previous import size for {import_name}")
        # results_diffs[import_name] = UNKNOWN_MARKER
        ignored_imports.append(import_name)
        continue
    elif current_size is None:
        print(f"Cannot calculate new import size for {import_name}")
        # results_diffs[import_name] = LOST_MARKER
        ignored_imports.append(import_name)
        continue
    elif original_size is None:
        print(f"Cannot calculate old import size for {import_name}")
        # results_diffs[import_name] = RETRACKED_MARKER
        ignored_imports.append(import_name)
        continue

    if current_size == original_size:
        print(f"No change in import size for {import_name}")
        continue

    size_diff = current_size - original_size
    size_growth = size_diff / original_size

    # results_diffs[import_name] = ImportStats(current_size, size_diff, size_growth)

    size_triggered = current_size >= SMALL_BOARD_THRESHOLD
    diff_triggered = size_diff >= GROWTH_AMOUNT_THRESHOLD
    mult_triggered = size_growth >= GROWTH_PERCENT_THRESHOLD

    changed_import_sizes[import_name] = ImportStats(
        original_size, current_size, size_diff, size_growth
    )

# Include newly added imports
for import_name in new_imports:
    current_size = results[import_name]

    if current_size is None:
        print(f"Cannot calculate growth for {import_name}")
        ignored_imports.append(import_name)
        continue

    # results_diffs[import_name] = ImportStats(current_size, 0, 0)

    added_import_sizes[import_name] = current_size

added_text = ""
if added_import_sizes:
    added_text = "The following imports were added that triggered warnings:\n\n"
    for import_name, import_size in added_import_sizes.items():
        added_text += f"- {import_name}: {import_size} bytes (small board warning)\n"
    added_text += "\n"

changed_text = ""
if changed_import_sizes:
    changed_text = "The following imports were changed and triggered warnings:\n\n"
    for import_name, import_stats in changed_import_sizes.items():
        changed_text += f"- {import_name}: {import_stats.original_size} -> {import_stats.current_size} bytes ({import_stats.diff} bytes, {round(import_stats.growth_percent * 100, 2)}% growth)\n"
    changed_text += "\n"

ignored_text = ""
if ignored_imports:
    ignored_text = "The following imports could not be measured and were ignored (see workflow artifacts):\n\n"
    for import_name in ignored_imports:
        ignored_text += f"- {import_name}\n"
    ignored_text += "\n"

analysis_text = added_text + changed_text + ignored_text

with open(analysis_filepath, mode="w") as analysis_file:
    analysis_file.write(analysis_text)
