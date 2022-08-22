#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2022 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""The install packages script"""
import re
import subprocess
import sys
from typing import List


def _load_dependencies(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return [i for i in f.readlines() if i]


RE = re.compile("(.*)[=><]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("not enought arguments")

    filename = sys.argv[1]
    packages = sys.argv[2:]
    requirements = _load_dependencies(filename)

    to_install = []
    for package in packages:
        for requirement in requirements:
            if re.match(f"^{package}([<>=].*)?$", requirement):
                to_install.append(requirement.strip())
    if not to_install:
        raise ValueError("No packages found to install")
    print("installing", ", ".join(to_install))
    subprocess.check_call([sys.executable, "-m", "pip", "install", *to_install])
