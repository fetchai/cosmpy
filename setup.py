#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
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

"""The setup script"""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = "0.5.1"

setup(
    name="cosmpy",
    version=VERSION,
    description="A library for interacting with the cosmos networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fetchai/cosmpy",
    author="Fetch.AI Limited",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="cosmos, gaia, fetchhub, fetchai",
    package_dir={"cosmpy": "cosmpy"},
    packages=find_packages(include=["cosmpy*"]),
    python_requires=">=3.6, <4",
    install_requires=[
        "ecdsa",
        "bech32",
        "requests",
        "protobuf>=3.19.4,<4",
        "grpcio==1.47.0",
        "bip-utils",
        "blspy",
        "google-api-python-client",
    ],
    extras_require={
        "dev": [
            "check-manifest",
            "tox==3.25.1",
            "flake8==5.0.4",
            "black==22.6",
            "mypy==0.971",
            "mkdocs-material==8.4",
            "bandit==1.7.4",
            "safety==2.1.1",
            "isort==5.10.1",
            "darglint==1.8.1",
            "vulture==2.5",
            "pylint==2.14.5",
            "liccheck==0.7.2",
            "flake8-copyright==0.2.3",
            "grpcio-tools==1.47.0",
            "flake8-bugbear==22.7.1",
            "flake8-eradicate==1.3.0",
            "flake8-docstrings==1.6.0",
            "pydocstyle==6.1.1",
            "pydoc-markdown==4.6.3",
        ],
        "test": ["coverage", "pytest", "pytest-rerunfailures"],
    },
    project_urls={
        "Bug Reports": "https://github.com/fetchai/cosmpy/issues",
        "Source": "https://github.com/fetchai/cosmpy",
    },
)
