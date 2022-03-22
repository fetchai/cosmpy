COSMOS_SDK_DIR := cosmos-sdk-proto-schema
WASMD_DIR := wasm-proto-shema
COSMOS_SDK_VERSION := v0.17.8
COSMOS_SDK_URL := https://github.com/fetchai/cosmos-sdk
WASMD_VERSION := v0.21.0
COSMOS_PROTO_RELATIVE_DIRS := proto third_party/proto
WASMD_PROTO_RELATIVE_DIRS := proto
SOURCES_REGEX_TO_EXCLUDE := third_party/proto/google/.*
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
        FIND_CMD := find $(COSMOS_PROTO_RELATIVE_DIRS) -regextype posix-extended
				OPEN_CMD := xdg-open
    endif
    ifeq ($(UNAME_S),Darwin)
        FIND_CMD := find -E $(COSMOS_PROTO_RELATIVE_DIRS)
				OPEN_CMD := open
    endif
endif

define unique
  $(eval seen :=)
  $(foreach _,$1,$(if $(filter $_,${seen}),,$(eval seen += $_)))
  ${seen}
endef
unique = $(if $1,$(firstword $1) $(call unique,$(filter-out $(firstword $1),$1)))


FIND_CMD := $(FIND_CMD) -type f -name *.proto $(SOURCES_REGEX_TO_EXCLUDE:%=! -regex "%")
RELATIVE_SOURCE := $(shell [ -d "$(COSMOS_SDK_DIR)" ] && { cd $(COSMOS_SDK_DIR) && $(FIND_CMD); })
UNROOTED_SOURCE := $(foreach _,$(COSMOS_PROTO_RELATIVE_DIRS),$(patsubst $(_)/%,%,$(filter $(_)/%,$(RELATIVE_SOURCE))))
SOURCE := $(RELATIVE_SOURCE:%=$(COSMOS_SDK_DIR)/%)
GENERATED := $(UNROOTED_SOURCE:%.proto=$(OUTPUT_FOLDER)/%.py)
PROTO_ROOT_DIRS := $(COSMOS_PROTO_RELATIVE_DIRS:%=$(COSMOS_SDK_DIR)/%)

GENERATED_DIRS := $(call unique,$(foreach _,$(UNROOTED_SOURCE),$(dir $(_))))
INIT_PY_FILES_TO_CREATE :=  $(GENERATED_DIRS:%=$(OUTPUT_FOLDER)/%__init__.py)

COMPILE_PROTOBUFS_COMMAND := python -m grpc_tools.protoc $(PROTO_ROOT_DIRS:%=--proto_path=%) --python_out=$(OUTPUT_FOLDER) --grpc_python_out=$(OUTPUT_FOLDER) $(UNROOTED_SOURCE)


generate_proto_types: $(COSMOS_SDK_DIR) $(WASMD_DIR)
	$(COMPILE_PROTOBUFS_COMMAND)

fetch_proto_schema_source: $(COSMOS_SDK_DIR) $(WASMD_DIR)

generate_init_py_files: $(INIT_PY_FILES_TO_CREATE)

$(SOURCE): $(COSMOS_SDK_DIR)

$(GENERATED): $(SOURCE)
	$(COMPILE_PROTOBUFS_COMMAND)

$(INIT_PY_FILES_TO_CREATE): $(GENERATED_DIRS)
	touch $(INIT_PY_FILES_TO_CREATE)

$(GENERATED_DIRS): $(COSMOS_SDK_DIR) $(WASMD_DIR)

$(COSMOS_SDK_DIR): Makefile
	rm -rfv $(COSMOS_SDK_DIR)
	git clone --branch $(COSMOS_SDK_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none $(COSMOS_SDK_URL) $(COSMOS_SDK_DIR)
	cd $(COSMOS_SDK_DIR) && git checkout $(COSMOS_SDK_VERSION) -- $(COSMOS_PROTO_RELATIVE_DIRS)

$(WASMD_DIR): Makefile
	rm -rfv $(WASMD_DIR)
	git clone --branch $(WASMD_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none https://github.com/CosmWasm/wasmd $(WASMD_DIR)
	cd $(WASMD_DIR) && git checkout $(WASMD_VERSION) -- $(WASMD_PROTO_RELATIVE_DIRS)
	cp -rpv $(WASMD_PROTO_RELATIVE_DIRS:%=$(WASMD_DIR)/%) $(COSMOS_SDK_DIR)

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
	vulture $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude '*_pb2.py,*_pb2_grpc.py'

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
	coverage run -m pytest $(PYCOSM_TESTS_DIR) --doctest-modules --ignore $(PYCOSM_TESTS_DIR)/vulture_whitelist.py -m "not integtest"

.PHONY: integration-test
integration-test:
	coverage run -m pytest $(PYCOSM_TESTS_DIR) --doctest-modules --ignore $(PYCOSM_TESTS_DIR)/vulture_whitelist.py -m "integtest"

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

.PHONY: generate-docs
generate-docs:
	sphinx-apidoc -f -o $(PYCOSM_DOCS_DIR)/source $(PYCOSM_SRC_DIR) $(PYCOSM_SRC_DIR)/vulture_whitelist.py
	cd $(PYCOSM_DOCS_DIR) && $(MAKE) html

# Open docs main page in default browser
.PHONY: open-docs
open-docs:
ifneq ($(wildcard $(PYCOSM_DOCS_DIR)/build),)
	$(OPEN_CMD) $(PYCOSM_DOCS_DIR)/build/html/index.html
else
	@echo "Built docs are not found. Please run '$(MAKE) generate-docs' first."
endif

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
	rm -fr docs/build/

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
	vulture $(PYCOSM_SRC_DIR) $(PYCOSM_TESTS_DIR) $(PYCOSM_EXAMPLES_DIR) setup.py --exclude '*_pb2.py,*_pb2_grpc.py'

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
