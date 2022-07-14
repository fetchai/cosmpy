#!/usr/bin/env python3
# This script requires `mdspell`:
#
#    https://www.npmjs.com/package/markdown-spellcheck
#
# Run this script from the root directory.
# Usage:
#   python scripts/spell-check.py
#

import os
import subprocess

MDSPELL_PATH = os.popen("which mdspell").read().rstrip("\n")
if str(MDSPELL_PATH) == "":
    print(
        "Cannot find executable 'mdspell'. Please install it to run this script: npm i markdown-spellcheck -g"
    )
    exit(127)
print("Found 'mdspell' executable at " + str(MDSPELL_PATH))
subprocess.call(["mdspell", "-n", "-a", "--en-gb", "**/*.md"])
