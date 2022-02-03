## Development setup

The easiest way to get set up for development is to install Python `>=3.7` and `pipenv`, then run the following:

```bash
  make new_env_dev
  pipenv shell
```

## Development commands

There are various makefile commands which are helpful during development. Some of the more prominent ones are listed below:

- For linting:
  ```bash
    make lint
  ```
- For static analysis:
  ```bash
    make mypy
    make pylint
  ```
- For code security analysis:
  ```bash
    make security
  ```

- To run tests:
  ```bash
    make test
  ```

## Generating python types from Cosmos SDK protobuf schemas

This library uses python types which are generated (using [Google's Protocol Buffers](https://developers.google.com/protocol-buffers/) compiler) from protocol buffer schemas in the [Cosmos SDK](https://github.com/cosmos/cosmos-sdk) and [WasmD](https://github.com/CosmWasm/wasmd).

When updating the Cosmos SDK version supported by this library (see the version currently used under `COSMOS_SDK_VERSION` in [Makefile](#Makefile])), you will need to fetch its corresponding protobuf schemas and generate their associated python types, replacing the existing ones.

>Note: This process has to be done only once when the Cosmos SDK version supported by this library is changed.

>Note: To generate python types from Cosmos SDK protobuf schemas, you will need [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) compiler. A guide on how to install it can be found [here](https://fetchai.github.io/oef-sdk-python/user/install.html#protobuf-compiler).

Below are the steps you need to take in order to achieve this:

* Fetch the Cosmos SDK protobuf schema files:
  ```bash
  make fetch_proto_schema_source
  ```

* Generate python types:
  ```bash
  make generate_proto_types
  ```

>Note: For this library to be functional, only the python types generated from protobuf schemas are required, not the schema files themselves.
> The schema files are fetched on-demand only to enable the generation of python types.
> Therefore, the schema files are intentionally stored as **local** files and are **NOT** checked in to this repository to minimise its filesystem footprint.

## MakeFile Commands

The Makefile in this repo provides various useful commands that ease development. We will describe some of them here:

* `make lint`:
  * applies `black`: code formatter
  * applies `isort`: sorts imports
  * runs `flake8`: linter
  * runs `vulture`: detects unused code
* `make security`:
  * runs `bandit`: finds common security issues in Python code
  * runs `safety`: checks installed dependencies for known security vulnerabilities
* `make mypy`: runs `mypy`, a static type checker for python
* `make pylint`: runs `pylint`, a static type checker and linter for python
* tests:
  * `make test`: runs all tests
  * `make unit-test`: runs unit tests
  * `make integration-test`: runs integration tests
  * `make coverage-report`: produces the coverage report (you should run tests using one of the above commands first)
* `make clean`: removes temporary files and caches.
* `make new_env`: creates a new environment (cleans and installs in _normal_ mode)
* `make new_env_dev`: creates a new development environment (cleans and installs in _development_ mode)
* `make liccheck`: checks dependencies and reports any license issues
* `make copyright-check`: checks that files have the correct copyright headers 
* documentation:
  * `make generate-docs`: generates documentation from the source code
  * `make open-docs`: opens `index.html` page of the documentation (if on Linux or MacOS).

## To setup a local Stargate node

### Preliminaries

You require Go version 16.0 or higher for your platform (see <a href="https://golang.org/doc/install" target="_blank">here</a>)

### Setup a node

- Setup FetchD
  ```bash
  bash scripts/setup_fetchd.sh
  ```
  The script will ask for root permissions while setting up a node.

- Start the node
  ```bash
  fetchd start
  ```

## To run a local Stargate node in docker

### Preliminaries

You require [Docker](https://docs.docker.com/get-docker/) for your platform. 

### Run the docker image

* Place the following entrypoint script somewhere in your system (e.g `~/fetchd_docker/fetchd_initialise.sh`):

  ```bash
  #!/usr/bin/env bash
  
  # variables
  export VALIDATOR_KEY_NAME=validator
  export BOB_KEY_NAME=bob
  export VALIDATOR_MNEMONIC="erase weekend bid boss knee vintage goat syrup use tumble device album fortune water sweet maple kind degree toss owner crane half useless sleep"
  export BOB_MNEMONIC="account snack twist chef razor sing gain birth check identify unable vendor model utility fragile stadium turtle sun sail enemy violin either keep fiction"
  export PASSWORD="12345678"
  export CHAIN_ID=testing
  export DENOM_1=stake
  export DENOM_2=atestfet
  
  # Add keys
  ( echo "$VALIDATOR_MNEMONIC"; echo "$PASSWORD"; echo "$PASSWORD"; ) |fetchd keys add $VALIDATOR_KEY_NAME --recover
  ( echo "$BOB_MNEMONIC"; echo "$PASSWORD"; ) |fetchd keys add $BOB_KEY_NAME --recover
  
  # Configure node
  fetchd init --chain-id=$CHAIN_ID $CHAIN_ID
  echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $VALIDATOR_KEY_NAME -a) 100000000000000000000000$DENOM_1
  echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $BOB_KEY_NAME -a) 100000000000000000000000$DENOM_2
  echo "$PASSWORD" |fetchd gentx $VALIDATOR_KEY_NAME 10000000000000000000000$DENOM_1 --chain-id $CHAIN_ID
  fetchd collect-gentxs
  
  # Enable rest-api
  sed -i '/^\[api\]$/,/^\[/ s/^enable = false/enable = true/' ~/.fetchd/config/app.toml
  sed -i '/^\[api\]$/,/^\[/ s/^swagger = false/swagger = true/' ~/.fetchd/config/app.toml
  
  fetchd start
  ```

* Execute:
  ```bash
  docker run -it --rm --entrypoint /scripts/<ENTRYPOINT_SCRIPT_NAME> -p 9090:9090 -p 1317:1317 -v <PATH_TO_ENTRYPOINT_SCRIPT>:/scripts/ fetchai/fetchd:0.9.0-rc4
  ```

where `<ENTRYPOINT_SCRIPT_NAME>` is the name of the entrypoint script (e.g.`fetchd_initialise.sh`) and `<PATH_TO_ENTRYPOINT_SCRIPT>` is the path to the directory you placed the script (e.g.`~/fetchd_docker/`).