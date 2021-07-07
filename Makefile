COSMOS_SDK_DIR := cosmos-sdk-proto-schema
COSMOS_SDK_VERSION := v0.17.1
OUTPUT_FOLDER := src

SOURCES_REGEX_TO_EXCLUDE := $(COSMOS_SDK_DIR)/third_party/proto/google/.*
PATTERNS_TO_EXCLUDE = $(patsubst %,! -regex "%",$(SOURCES_REGEX_TO_EXCLUDE))
SOURCE := $(shell find -E $(COSMOS_SDK_DIR) -type f -name *.proto $(PATTERNS_TO_EXCLUDE))
RELATIVE_SOURCE := $(foreach file,$(SOURCE),$(shell echo -n $(file) | sed -E 's|^([^/]+/)*proto/||'))
#RELATIVE_SOURCE := $(SOURCE)
RELATIVE_GENERATED := $(patsubst %.proto,$(OUTPUT_FOLDER)/%.py,$(RELATIVE_SOURCE))
PROTO_ROOT_DIRS := $(shell find -E $(COSMOS_SDK_DIR) -type d -regex "^([^/]+/)*proto" ! -regex "$(RELATIVE_SOURCE_EXCLUDE)(/.*)?")

define unique
  $(eval seen :=)
  $(foreach _,$1,$(if $(filter $_,${seen}),,$(eval seen += $_)))
  ${seen}
endef
unique = $(if $1,$(firstword $1) $(call unique,$(filter-out $(firstword $1),$1)))

#GENERATED_DIRS := $(shell find -E $(OUTPUT_FOLDER) -type d)
GENERATED_DIRS := $(call unique,$(patsubst %/,$(OUTPUT_FOLDER)/%,$(dir $(RELATIVE_SOURCE))))
INIT_PY_FILES_TO_CREATE :=  $(patsubst %,%/__init__.py,$(GENERATED_DIRS))

COMPILE_PROTOBUFS_COMMAND := protoc $(patsubst %,--proto_path=%,$(PROTO_ROOT_DIRS)) --python_out=$(OUTPUT_FOLDER) $(RELATIVE_SOURCE)


generate_proto_types: $(SOURCE)
	$(COMPILE_PROTOBUFS_COMMAND)

fetch_proto_schema_source: $(COSMOS_SDK_DIR)

generate_init_py_files: $(INIT_PY_FILES_TO_CREATE)

$(SOURCE)&: $(COSMOS_SDK_DIR)

$(RELATIVE_GENERATED)&: $(SOURCE)
	$(COMPILE_PROTOBUFS_COMMAND)

$(INIT_PY_FILES_TO_CREATE)&: $(GENERATED_DIRS)
	touch $(INIT_PY_FILES_TO_CREATE)

$(GENERATED_DIRS)&: $(COSMOS_SDK_DIR)

$(COSMOS_SDK_DIR): Makefile
	rm -rf $(COSMOS_SDK_DIR)
	git clone --branch $(COSMOS_SDK_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none https://github.com/fetchai/cosmos-sdk $(COSMOS_SDK_DIR)
	cd $(COSMOS_SDK_DIR) && git checkout $(COSMOS_SDK_VERSION) -- proto third_party/proto

debug:
	$(info SOURCES_REGEX_TO_EXCLUDE: $(SOURCES_REGEX_TO_EXCLUDE))
	$(info  )
	$(info PATTERNS_TO_EXCLUDE: $(PATTERNS_TO_EXCLUDE))
	$(info  )
	$(info GENERATED_DIRS: $(GENERATED_DIRS))
	$(info  )
	$(info INIT_PY_FILES_TO_CREATE: $(INIT_PY_FILES_TO_CREATE))
	$(info  )
	$(info SOURCE: $(SOURCE))
	$(info  )
	$(info RELATIVE_SOURCE: $(RELATIVE_SOURCE))
	$(info  )
	$(info RELATIVE_GENERATED: $(RELATIVE_GENERATED))
	$(info  )
	$(info PROTO_ROOT_DIRS: $(PROTO_ROOT_DIRS))
