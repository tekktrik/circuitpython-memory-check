import pathlib
import sys

import_name = sys.argv[1]

code_file = pathlib.Path("CIRCUITPY/code.py")
code_text = (
    "import gc\n"
    "pre = gc.mem_free()\n"
    f"import {import_name}\n"
    "post = gc.mem_free()\n"
    "used = pre - post\n"
    "print(used)"
)
with open(code_file, mode="w") as code_fp:
    code_fp.write(code_text)
