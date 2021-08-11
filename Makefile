COSMOS_SDK_DIR := cosmos-sdk-proto-schema
WASMD_DIR := wasm-proto-shema
COSMOS_SDK_VERSION := v0.17.1
WASMD_VERSION := v0.16.0
COSMOS_PROTO_RELATIVE_DIRS := proto third_party/proto
WASMD_PROTO_RELATIVE_DIRS := proto
SOURCES_REGEX_TO_EXCLUDE := third_party/proto/google/.*
OUTPUT_FOLDER := src
PYCOSM_SRC_DIR := src/cosm
PYCOSM_TESTS_DIR := tests
PYCOSM_EXAMPLES_DIR := examples

ifeq ($(OS),Windows_NT)
	$(error "Please use the WSL (Windows Subsystem for Linux) on Windows platform.")
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        FIND_CMD := find $(COSMOS_PROTO_RELATIVE_DIRS) -regextype posix-extended
    endif
    ifeq ($(UNAME_S),Darwin)
        FIND_CMD := find -E $(COSMOS_PROTO_RELATIVE_DIRS)
    endif
endif

define unique
  $(eval seen :=)
  $(foreach _,$1,$(if $(filter $_,${seen}),,$(eval seen += $_)))
  ${seen}
endef
unique = $(if $1,$(firstword $1) $(call unique,$(filter-out $(firstword $1),$1)))


FIND_CMD := $(FIND_CMD) -type f -name *.proto $(SOURCES_REGEX_TO_EXCLUDE:%=! -regex "%")
RELATIVE_SOURCE := $(shell cd $(COSMOS_SDK_DIR) && $(FIND_CMD))
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
	git clone --branch $(COSMOS_SDK_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none https://github.com/fetchai/cosmos-sdk $(COSMOS_SDK_DIR)
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
	tox -e black-check

.PHONY: isort-check
isort-check:
	tox -e isort-check

.PHONY: flake
flake:
	tox -e flake8

.PHONY: vulture
vulture:
	tox -e vulture

####################
### Security & Safety
####################

.PHONY: bandit
bandit:
	tox -e bandit

.PHONY: safety
safety:
	tox -e safety

####################
### Linters
####################

.PHONY: mypy
mypy:
	tox -e mypy

.PHONY: pylint
pylint:
	tox -e pylint

####################
### Tests
####################

.PHONY: test
test:
	tox -e test

####################
### License and copyright checks
####################

.PHONY: liccheck
liccheck:
	tox -e liccheck

.PHONY: copyright-check
copyright-check:
	tox -e copyright-check

####################
### Combinations
####################

.PHONY: lint
lint:
	tox -e black
	tox -e isort
	tox -e flake8
	tox -e vulture

.PHONY: check
check:
	make black-check
	make isort-check
	make flake
	make vulture
	make bandit
	make safety
	make mypy
	make pylint
	make liccheck
	make copyright-check
	make test

# Freeze deps to requirements.txt (needed for some Tox checks)
.PHONY: check
freeze:
	pipenv lock -r > requirements.txt

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
