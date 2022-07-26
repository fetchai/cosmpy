COSMOS_SDK_URL := https://github.com/fetchai/cosmos-sdk
COSMOS_SDK_VERSION := v0.18.0
COSMOS_SDK_DIR := build/cosmos-sdk-proto-schema

WASMD_URL := https://github.com/CosmWasm/wasmd
WASMD_VERSION := v0.24.0
WASMD_DIR := build/wasm-proto-shema

IBCGO_URL := https://github.com/cosmos/ibc-go
IBCGO_VERSION := v2.2.0
IBCGO_DIR := build/ibcgo-proto-schema

OUTPUT_FOLDER := cosmpy/protos
PYCOSM_SRC_DIR := cosmpy
PYCOSM_DOCS_DIR := docs

PYCOSM_TESTS_DIR := tests
PYCOSM_EXAMPLES_DIR := examples
REQUIREMENTS_FILES := requirements.txt requirements-dev.txt

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

generate_proto_types: $(COSMOS_SDK_DIR) $(WASMD_DIR) $(IBCGO_DIR)
	rm -fr $(OUTPUT_FOLDER)/*
	python -m grpc_tools.protoc --proto_path=$(WASMD_DIR)/proto --proto_path=$(WASMD_DIR)/third_party/proto  --python_out=$(OUTPUT_FOLDER) --grpc_python_out=$(OUTPUT_FOLDER) $(shell find $(WASMD_DIR) \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)
	python -m grpc_tools.protoc --proto_path=$(IBCGO_DIR)/proto --proto_path=$(IBCGO_DIR)/third_party/proto  --python_out=$(OUTPUT_FOLDER) --grpc_python_out=$(OUTPUT_FOLDER) $(shell find $(IBCGO_DIR) \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)
# ensure cosmos-sdk is last as previous modules may have duplicated proto models which are now outdated
	python -m grpc_tools.protoc --proto_path=$(COSMOS_SDK_DIR)/proto --proto_path=$(COSMOS_SDK_DIR)/third_party/proto  --python_out=$(OUTPUT_FOLDER) --grpc_python_out=$(OUTPUT_FOLDER) $(shell find $(COSMOS_SDK_DIR) \( -path */proto/* -or -path */third_party/proto/* \) -type f -name *.proto)

fetch_proto_schema_source: $(COSMOS_SDK_DIR) $(WASMD_DIR) $(IBCGO_DIR)

.PHONY: generate_init_py_files
generate_init_py_files: generate_proto_types
	find $(OUTPUT_FOLDER)/ -type d -exec touch {}/__init__.py \;
# restore root __init__.py as it contains code to have the proto files module available
	git restore $(OUTPUT_FOLDER)/__init__.py

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

####################
### Code style
####################

.PHONY: black-check
black-check:
	black --check --verbose $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude $(OUTPUT_FOLDER)

.PHONY: isort-check
isort-check:
	isort --check-only --verbose $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py

.PHONY: flake
flake:
	flake8 $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py

.PHONY: vulture
vulture:
	vulture $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude '*_pb2.py,*_pb2_grpc.py' --min-confidence 100

####################
### Security & Safety
####################

.PHONY: bandit
bandit:
	bandit -r $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) --skip B101
	bandit -r $(PYCOSM_EXAMPLES_DIR) --skip B101,B105

.PHONY: safety
safety:
	safety check -i 41002

####################
### Linters
####################

.PHONY: mypy
mypy:
	mypy $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py

.PHONY: pylint
pylint:
	pylint $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py

####################
### Tests
####################

.PHONY: test
test:
	coverage run -m pytest $(PYCOSM_TESTS_DIR) --doctest-modules --ignore $(PYCOSM_TESTS_DIR)/vulture_whitelist.py
	$(MAKE) coverage-report

.PHONY: unit-test
unit-test:
	coverage run -m pytest $(PYCOSM_TESTS_DIR) --doctest-modules --ignore $(PYCOSM_TESTS_DIR)/vulture_whitelist.py -m "not integration"

.PHONY: integration-test
integration-test:
	coverage run -m pytest $(PYCOSM_TESTS_DIR) --doctest-modules --ignore $(PYCOSM_TESTS_DIR)/vulture_whitelist.py -m "integration"

.PHONY: coverage-report
coverage-report:
	coverage report -m
	coverage html

####################
### License and copyright checks
####################

.PHONY: liccheck
liccheck:
	liccheck -s strategy.ini -r requirements.txt -l PARANOID

.PHONY: copyright-check
copyright-check:
	python scripts/check_copyright.py

####################
### Docs generation
####################

.PHONY: docs
docs:
	mkdocs build --clean


.PHONY: docs-live
docs-live:
	mkdocs serve

####################
### Clean and init commands
####################

.PHONY: clean
clean: clean-build clean-pyc clean-test

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
	rm -fr coverage_report/
	rm -fr .hypothesis
	rm -fr .pytest_cache
	rm -fr .mypy_cache/
	find . -name 'log.txt' -exec rm -fr {} +
	find . -name 'log.*.txt' -exec rm -fr {} +

v := $(shell pip -V | grep virtualenvs)

.PHONY: new_env
new_env: clean
	if [ -z "$v" ];\
	then\
		pipenv --rm;\
		pipenv install --python 3.9;\
		echo "Enter virtual environment with all development dependencies now: 'pipenv shell'.";\
	else\
		echo "In a virtual environment! Exit first: 'exit'.";\
	fi

.PHONY: new_env_dev
new_env_dev: clean
	if [ -z "$v" ];\
	then\
		pipenv --rm;\
		pipenv install --python 3.9 --dev --skip-lock --clear;\
		echo "Enter virtual environment with all development dependencies now: 'pipenv shell'.";\
	else\
		echo "In a virtual environment! Exit first: 'exit'.";\
	fi

####################
### Combinations
####################

.PHONY: lint
lint:
	black $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude $(OUTPUT_FOLDER)
	isort $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py
	flake8 $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py
	vulture $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude '*_pb2.py,*_pb2_grpc.py' --min-confidence 100
	darglint aerial auth bank common cosmwasm crypto distribution evidence gov ibc mint params slashing staking tendermint tx upgrade

.PHONY: security
security:
	bandit -r $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) --skip B101
	bandit -r $(PYCOSM_EXAMPLES_DIR) --skip B101,B105
	safety check -i 41002


.PHONY: check
check:
	$(MAKE) black-check
	$(MAKE) isort-check
	$(MAKE) flake
	$(MAKE) vulture
	$(MAKE) bandit
	$(MAKE) safety
	$(MAKE) mypy
	$(MAKE) pylint
	$(MAKE) liccheck
	$(MAKE) copyright-check
	$(MAKE) test

Pipfile.lock: Pipfile setup.py
	pipenv lock --dev

requirements.txt: Pipfile.lock
	pipenv lock -r > $@

requirements-dev.txt: Pipfile.lock
	pipenv lock -r --dev > $@

.PHONY: requirements
requirements: $(REQUIREMENTS_FILES)

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
