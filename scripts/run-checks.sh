#!/bin/bash
set -e

echo Running black-check ...
tox -e black-check
echo Running black-check ... complete

echo Running isort-check ...
tox -e isort-check
echo Running isort-check ... complete

echo Running flake8 ...
tox -e flake8
echo Running flake8 ... complete

echo Running mypy ...
tox -e mypy
echo Running mypy ... complete

echo Running vulture ...
tox -e vulture
echo Running vulture ... complete

echo Running bandit ...
tox -e bandit
echo Running bandit ... complete

echo Running safety ...
tox -e safety
echo Running safety ... complete

echo Running liccheck ...
tox -e liccheck
echo Running liccheck ... complete

echo Running copyright-check ...
tox -e copyright-check
echo Running copyright-check ... complete

echo Running test ...
tox -e test
echo Running test ... complete

echo Running coverage-report ...
tox -e coverage-report
echo Running coverage-report ... complete

echo 'Great Success - all done!'