#!/bin/bash
set -e

echo Running Black...
tox -e black

echo Running Black...
tox -e isort