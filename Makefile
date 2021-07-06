COSMOS_SDK_DIR := cosmos-sdk-proto-schema
COSMOS_SDK_VERSION := v0.17.1
OUTPUT_FOLDER := src/cosm/types

SOURCE := $(shell find $(COSMOS_SDK_DIR) -type f -name *.proto)
RELATIVE_SOURCE := $(foreach file,$(SOURCE),$(shell echo -n $(file) | sed -E 's|^([^/]+/)*proto/||'))
RELATIVE_GENERATED := $(patsubst %.proto,$(types_folder)/%.py,$(RELATIVE_SOURCE))
PROTO_ROOT_DIRS := $(shell find -E $(COSMOS_SDK_DIR) -type d -regex "^([^/]+/)*proto")

GENERATED_DIRS := $(shell find -E $(OUTPUT_FOLDER) -type d)
INIT_PY_FILES_TO_CREATE :=  $(patsubst %,%/__init__.py,$(GENERATED_DIRS))

COMMAND := protoc $(patsubst %,--proto_path=%,$(PROTO_ROOT_DIRS)) --python_out=$(OUTPUT_FOLDER) $(RELATIVE_SOURCE) && touch $(INIT_PY_FILES_TO_CREATE)


generate_proto_types: $(SOURCE)
	@echo $(COMMAND)
	$(COMMAND)

$(RELATIVE_GENERATED) &: $(SOURCE)
	@echo $(COMMAND)
	$(COMMAND)

$(SOURCE) &:
	make $(COSMOS_SDK_DIR)

$(COSMOS_SDK_DIR):
	git clone --branch $(COSMOS_SDK_VERSION) --depth 1 --quiet --no-checkout --filter=blob:none https://github.com/fetchai/cosmos-sdk $(COSMOS_SDK_DIR)
	cd $(COSMOS_SDK_DIR) && git checkout $(COSMOS_SDK_VERSION) -- proto third_party/proto

fetch_proto_schema_source:
	rm -rf $(COSMOS_SDK_DIR)
	make $(COSMOS_SDK_DIR)

debug: $(SOURCE)
	$(info SOURCE is $(SOURCE))
	$(info RELATIVE_SOURCE is $(RELATIVE_SOURCE))
	$(info RELATIVE_GENERATED is $(RELATIVE_GENERATED))
	$(info PROTO_ROOT_DIRS is $(PROTO_ROOT_DIRS))
