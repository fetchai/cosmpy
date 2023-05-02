COSMOS_SDK_URL := https://github.com/cosmos/cosmos-sdk
COSMOS_SDK_VERSION := v0.46.10
COSMOS_SDK_DIR := build/cosmos-sdk-proto-schema

WASMD_URL := https://github.com/CosmWasm/wasmd
WASMD_VERSION := v0.27.0
WASMD_DIR := build/wasm-proto-shema

IBCGO_URL := https://github.com/cosmos/ibc-go
IBCGO_VERSION := v5.2.0
IBCGO_DIR := build/ibcgo-proto-schema

C4E_URL := https://github.com/chain4energy/c4e-chain
C4E_VERSION := v1.2.0
C4E_DIR := build/c4e-proto-schema

COSMPY_PROTOS_DIR := cosmpy/protos
COSMPY_SRC_DIR := cosmpy
COSMPY_TESTS_DIR := tests
COSMPY_EXAMPLES_DIR := examples
COSMPY_SCRIPTS_DIR := scripts

PYTHON_CODE_DIRS := $(COSMPY_SRC_DIR) $(COSMPY_TESTS_DIR) $(COSMPY_EXAMPLES_DIR) $(COSMPY_SCRIPTS_DIR)

########################################
### Initialise dev environment
########################################

# Create a new poetry virtual environment with all the necessary dependencies installed.
# Once finished, `poetry shell` to enter the virtual environment
v := $(shell pip -V | grep virtualenvs)

.PHONY: new-env
new-env: clean
	if [ -z "$v" ];\
	then\
		poetry install --with main,dev,test,docs;\
		echo "Enter virtual environment with all development dependencies now: 'poetry shell'.";\
	else\
		echo "In a virtual environment! Exit first: 'exit'.";\
	fi

########################################
### Tests
########################################

# Run all tests
.PHONY: test
test:
	coverage run -m pytest $(COSMPY_TESTS_DIR) --doctest-modules
	$(MAKE) coverage-report

# Run all unit tests
.PHONY: unit-test
unit-test:
	coverage run -m pytest $(COSMPY_TESTS_DIR) --doctest-modules -m "not integration"

# Run all integration tests
.PHONY: integration-test
integration-test:
	coverage run -m pytest $(COSMPY_TESTS_DIR) --doctest-modules -m "integration"

# Produce the coverage report. Can see a report summary on the terminal.
# Detailed report on all modules are placed under /coverage-report
.PHONY: coverage-report
coverage-report:
	coverage report -m
	coverage html

########################################
### Code Styling
########################################

# Automatically run black and isort to format the code, and run flake8 and vulture checks
.PHONY: lint
lint: black isort flake8 vulture

# Automatically format the code using black
.PHONY: black
black:
	black $(PYTHON_CODE_DIRS) --exclude $(COSMPY_PROTOS_DIR)

# Automatically sort the imports
.PHONY: isort
isort:
	isort $(PYTHON_CODE_DIRS)

# Check the code format
.PHONY: black-check
black-check:
	black --check --verbose $(PYTHON_CODE_DIRS) --exclude $(COSMPY_PROTOS_DIR)

# Check the imports are sorted
.PHONY: isort-check
isort-check:
	isort --check-only --verbose $(PYTHON_CODE_DIRS)

# Run flake8 linter
.PHONY: flake8
flake8:
	flake8 $(PYTHON_CODE_DIRS)

# Check for unused code
.PHONY: vulture
vulture:
	vulture $(PYTHON_CODE_DIRS) scripts/whitelist.py --exclude '*_pb2.py,*_pb2_grpc.py' --min-confidence 100

########################################
### Security & safety checks
########################################

# Run bandit and safety
.PHONY: security
security: bandit safety

# Check the security of the code
.PHONY: bandit
bandit:
	bandit -r $(COSMPY_SRC_DIR) $(COSMPY_TESTS_DIR) -s B101
	bandit -r $(COSMPY_EXAMPLES_DIR) -s B101,B105

# Check the security of the code for known vulnerabilities
.PHONY: safety
safety:
	safety check -i 41002

########################################
### Linters
########################################

# Check types (statically) using mypy
.PHONY: mypy
mypy:
	mypy $(PYTHON_CODE_DIRS) --exclude $(COSMPY_PROTOS_DIR)

# Lint the code using pylint
.PHONY: pylint
pylint:
	pylint -j 0 $(PYTHON_CODE_DIRS)

########################################
### License and copyright checks
########################################

# Check dependency licenses
.PHONY: liccheck
liccheck:
	poetry export > tmp-requirements.txt
	liccheck -s strategy.ini -r tmp-requirements.txt -l PARANOID
	rm -frv tmp-requirements.txt

# Check that the relevant files have appropriate Copyright header
.PHONY: copyright-check
copyright-check:
	python scripts/check_copyright.py --directory .

########################################
### Docs
########################################

# Build documentation
.PHONY: docs
docs:
	mkdocs build --clean

# Live documentation server
.PHONY: docs-live
docs-live:
	mkdocs serve

# Generate API documentation (ensure you add the new pages created into /mkdocs.yml --> nav)
.PHONY: generate-api-docs
generate-api-docs:
	python3 scripts/generate_api_docs.py

########################################
### Poetry Lock
########################################

# Updates the poetry lock
poetry.lock: pyproject.toml
	poetry lock

########################################
### Clear the caches and temporary files
########################################

# clean the caches and temporary files and directories
.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docs

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr pip-wheel-metadata
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

.PHONY: clean-docs
clean-docs:
	rm -fr site/

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.DS_Store' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -f .coverage
	find . -name ".coverage*" -not -name ".coveragerc" -exec rm -fr "{}" \;
	rm -fr coverage.xml
	rm -fr htmlcov/
	rm -fr .hypothesis
	rm -fr .pytest_cache
	rm -fr .mypy_cache/
	find . -name 'log.txt' -exec rm -fr {} +
	find . -name 'log.*.txt' -exec rm -fr {} +

########################################
### Build
########################################

# Build the project
.PHONY: dist
dist: clean
	poetry build

########################################
### Generate protos and grpc files
########################################

ifeq ($(OS),Windows_NT)
	$(error "Please use the WSL (Windows Subsystem for Linux) on Windows platform.")
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
		OPEN_CMD := xdg-open
    endif
    ifeq ($(UNAME_S),Darwin)
		OPEN_CMD := open
    endif
endif

define unique
  $(eval seen :=)
  $(foreach _,$1,$(if $(filter $_,${seen}),,$(eval seen += $_)))
  ${seen}
endef
unique = $(if $1,$(firstword $1) $(call unique,$(filter-out $(firstword $1),$1)))

proto: fetch_proto_schema_source generate_proto_types generate_init_py_files

generate_proto_types: $(COSMOS_SDK_DIR) $(WASMD_DIR) $(IBCGO_DIR) $(C4E_DIR)
	rm -frv $(COSMPY_PROTOS_DIR)/*
	# python3 -m grpc_tools.protoc --proto_path=$(WASMD_DIR)/proto --proto_path=$(WASMD_DIR)/third_party/proto  --python_out=$(COSMPY_PROTOS_DIR) --grpc_python_out=$(COSMPY_PROTOS_DIR) $(shell find $(WASMD_DIR) \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)
	python3 -m grpc_tools.protoc --proto_path=$(IBCGO_DIR)/proto --proto_path=$(IBCGO_DIR)/third_party/proto  --python_out=$(COSMPY_PROTOS_DIR) --grpc_python_out=$(COSMPY_PROTOS_DIR) $(shell find $(IBCGO_DIR) \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)
# ensure cosmos-sdk is last as previous modules may have duplicated proto models which are now outdated
	python3 -m grpc_tools.protoc --proto_path=$(COSMOS_SDK_DIR)/proto --proto_path=$(COSMOS_SDK_DIR)/third_party/proto  --proto_path=$(IBCGO_DIR)/third_party/proto --python_out=$(COSMPY_PROTOS_DIR) --grpc_python_out=$(COSMPY_PROTOS_DIR) $(shell find $(COSMOS_SDK_DIR) $(IBCGO_DIR)/third_party/proto/gogoproto \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)
	# other chains modules
	python3 -m grpc_tools.protoc --proto_path=$(COSMOS_SDK_DIR)/proto --proto_path=$(IBCGO_DIR)/third_party/proto --proto_path=$(C4E_DIR)/proto --python_out=$(COSMPY_PROTOS_DIR) --grpc_python_out=$(COSMPY_PROTOS_DIR) $(shell find $(C4E_DIR) $(IBCGO_DIR)/third_party/proto/gogoproto  \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)

fetch_proto_schema_source: $(COSMOS_SDK_DIR) $(WASMD_DIR) $(IBCGO_DIR) $(C4E_DIR)

.PHONY: generate_init_py_files
generate_init_py_files: generate_proto_types
	find $(COSMPY_PROTOS_DIR)/ -type d -exec touch {}/__init__.py \;
# restore root __init__.py as it contains code to have the proto files module available
	git restore $(COSMPY_PROTOS_DIR)/__init__.py

$(SOURCE): $(COSMOS_SDK_DIR)

$(GENERATED): $(SOURCE)
	$(COMPILE_PROTOBUFS_COMMAND)

$(INIT_PY_FILES_TO_CREATE): $(GENERATED_DIRS)
	touch $(INIT_PY_FILES_TO_CREATE)

$(GENERATED_DIRS): $(COSMOS_SDK_DIR) $(WASMD_DIR) $(IBCGO_DIR)

$(COSMOS_SDK_DIR): Makefile
	rm -rfv $(COSMOS_SDK_DIR)
	git clone --branch $(COSMOS_SDK_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none $(COSMOS_SDK_URL) $(COSMOS_SDK_DIR)
	cd $(COSMOS_SDK_DIR) && git checkout $(COSMOS_SDK_VERSION) -- $(COSMOS_PROTO_RELATIVE_DIRS)

$(WASMD_DIR): Makefile
	rm -rfv $(WASMD_DIR)
	git clone --branch $(WASMD_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none $(WASMD_URL) $(WASMD_DIR)
	cd $(WASMD_DIR) && git checkout $(WASMD_VERSION) -- $(WASMD_PROTO_RELATIVE_DIRS)

$(IBCGO_DIR): Makefile
	rm -rfv $(IBCGO_DIR)
	git clone --branch $(IBCGO_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none $(IBCGO_URL) $(IBCGO_DIR)
	cd $(IBCGO_DIR) && git checkout $(IBCGO_VERSION) -- $(IBCGO_PROTO_RELATIVE_DIRS)

$(C4E_DIR): Makefile
	rm -rfv $(C4E_DIR)
	git clone --branch $(C4E_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none $(C4E_URL) $(C4E_DIR)
	cd $(C4E_DIR) && git checkout $(C4E_VERSION) -- $(C4E_PROTO_RELATIVE_DIRS)

debug:
	$(info SOURCES_REGEX_TO_EXCLUDE: $(SOURCES_REGEX_TO_EXCLUDE))
	$(info  )
	$(info GENERATED_DIRS: $(GENERATED_DIRS))
	$(info  )
	$(info INIT_PY_FILES_TO_CREATE: $(INIT_PY_FILES_TO_CREATE))
	$(info  )
	$(info SOURCE: $(SOURCE))
	$(info  )
	$(info RELATIVE_SOURCE: $(RELATIVE_SOURCE))
	$(info  )
	$(info GENERATED: $(GENERATED))
	$(info  )
	$(info UNROOTED_SOURCE: $(UNROOTED_SOURCE))
	$(info  )
	$(info PROTO_ROOT_DIRS: $(PROTO_ROOT_DIRS))
	$(info  )
	$(info FIND_CMD: $(FIND_CMD))
	$(info  )
	$(info COMPILE_PROTOBUFS_COMMAND: $(COMPILE_PROTOBUFS_COMMAND))

########################################
### Commands used by CI workflows
########################################

# Live documentation server
.PHONY: docs-live-ci
docs-live-ci:
	mkdocs serve -a localhost:8080

# Produce the coverage report
.PHONY: coverage-report-ci
coverage-report-ci:
	coverage report -m -i

# Check MANIFEST.in file for completeness
.PHONY: check-manifest-ci
check-manifest-ci:
	check-manifest

# Check API documentation is up-to-date
.PHONY: check-api-docs-ci
check-api-docs-ci:
	python scripts/generate_api_docs.py --check-clean