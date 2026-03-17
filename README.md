# circuitpython-memory-check
Import a CircuitPython library and check the amount of RAM used

## prepare

Build the nativesim firmware (or use a cached version if available)

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``version`` | Version of CircuitPython to simulate | ``latest`` | Must be a version that supports the Zephyr OS native sim |
| ``circuitpython-folder`` | Folder name to use for the CircuitPython checkout | ``cpysim`` | Change this if it conflicts with another file/folder |

### Outputs

None

## analyze

Analyze the library's import memory usage

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``version`` | Version of CircuitPython to simulate | ``latest`` | Must be a version that supports the Zephyr OS native sim |
| ``branch`` | Name of repository branch to analyze | ``''`` |  |
| ``results-filename`` | Filename for the results file should be written (as a JSON file) | ``results.json`` |  |

### Outputs

None

## compare

Compare two memory analyses

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``results-filename`` | Filename for the new (changed) import analysis results file | ``results.json`` |  |
| ``original-results-filename`` | Filename for the unchanged (previous) import analysis results file | ``original_results.json`` |  |
| ``analysis-results-filename`` | Filename for the created analysis results file | ``memory_analysis.txt`` |  |

### Outputs

None
