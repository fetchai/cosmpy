[comment]: <> (  <a href="">)
[comment]: <> (    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fetchai/cosmpy">)
[comment]: <> (  </a>)

  <a href="https://img.shields.io/badge/lint-flake8-blueviolet">
    <img alt="flake8" src="https://img.shields.io/badge/lint-flake8-yellow" >
  </a>
  <a href="https://github.com/python/mypy">
    <img alt="mypy" src="https://img.shields.io/badge/static%20check-mypy-blue">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Black" src="https://img.shields.io/badge/code%20style-black-black">
  </a>
  <a href="https://github.com/PyCQA/bandit">
    <img alt="mypy" src="https://img.shields.io/badge/security-bandit-lightgrey">
  </a>

## Development setup

The easiest way to get set up for development is to install Python `>=3.7` and `pipenv`, then run the following:

```bash
  make new_env_dev
  pipenv shell
```

## Development commands

There are various makefile commands that help the development. Some of them are:

- For linting:

  ```bash
    make lint
  ```

- For static analysis:

  ```bash
    make mypy
    make pylint
  ```

- To run tests:

  ```bash
    make test
  ```
  
Before committing and opening a PR, use the above commands to run the checks locally. This saves CI hours and ensures you only commit clean code.

## Generating python types from Cosmos SDK protobuf schemas

This library uses python types which are generated (using [Google's Protocol Buffers](https://developers.google.com/protocol-buffers/) compiler) from protocol buffer schemas in the [Cosmos SDK](https://github.com/cosmos/cosmos-sdk) and [WasmD](https://github.com/CosmWasm/wasmd).

When updating the Cosmos-SDK version that is supported by this library (see the version currently used under `COSMOS_SDK_VERSION` in [Makefile](Makefile), you will need to fetch its corresponding protobuf schemas and generate their associated python types, replacing the existing ones.

> Note: This process has to be done only once when the Cosmos-SDK version supported by this library is changed.

> Note: To generate python types from Cosmos-SDK protobuf schemas, you will need [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) compiler. A guide on how to install it can be found [here](https://fetchai.github.io/oef-sdk-python/user/install.html#protobuf-compiler).

- To regenerate the protobuf schema files, run the following:

  ```bash
  make proto
  ```

>Note: For this library to be functional, only the python types generated from protobuf schemas are required, not the schema files themselves.
> The schema files are fetched on-demand only to enable the generation of python types.
> Therefore, the schema files are intentionally stored as **local** files and are **NOT** checked in to this repository to minimise its filesystem footprint.

## MakeFile Commands

The Makefile in this repo provides various useful commands that ease development. We will describe some of them here:

- `make lint`:
  - applies `black`: code formatter
  - applies `isort`: sorts imports
  - runs `flake8`: linter
  - runs `vulture`: detects unused code
- `make security`:
  - runs `bandit`: finds common security issues in Python code
  - runs `safety`: checks installed dependencies for known security vulnerabilities
- `make mypy`: runs `mypy`, a static type checker for python
- `make pylint`: runs `pylint`, a static type checker and linter for python
- tests:
  - `make test`: runs all tests
  - `make unit-test`: runs unit tests
  - `make integration-test`: runs integration tests
  - `make coverage-report`: produces the coverage report (you should run tests using one of the above commands first)
- `make clean`: removes temporary files and caches.
- `make new_env`: creates a new environment (cleans and installs in _normal_ mode)
- `make new_env_dev`: creates a new development environment (cleans and installs in _development_ mode)
- `make liccheck`: checks dependencies and reports any license issues
- `make copyright-check`: checks that files have the correct copyright headers
- documentation:
  - `make docs`: generates documentation from the source code
  - `make docs-live`: creates a live-reloading docs server on localhost.

## To set up a local Fetchai node

To set up a local Fetchai node refer to [this guide](https://docs.fetch.ai/ledger_v2/single-node-network/).

## To run a local Fetchai node in docker

### Preliminaries

You require [Docker](https://docs.docker.com/get-docker/) for your platform.

### Run the docker image

- Place the following entrypoint script somewhere in your system (e.g `~/fetchd_docker/fetchd_initialise.sh`):

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
  export MONIKER=some-moniker


  # Add keys
  ( echo "$VALIDATOR_MNEMONIC"; echo "$PASSWORD"; echo "$PASSWORD"; ) |fetchd keys add $VALIDATOR_KEY_NAME --recover
  ( echo "$BOB_MNEMONIC"; echo "$PASSWORD"; ) |fetchd keys add $BOB_KEY_NAME --recover

  # Configure node
  fetchd init --chain-id=$CHAIN_ID $MONIKER
  echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $VALIDATOR_KEY_NAME -a) 100000000000000000000000$DENOM_1
  echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $BOB_KEY_NAME -a) 100000000000000000000000$DENOM_2
  echo "$PASSWORD" |fetchd gentx $VALIDATOR_KEY_NAME 10000000000000000000000$DENOM_1 --chain-id $CHAIN_ID
  fetchd collect-gentxs

  # Enable rest-api
  sed -i '/^\[api\]$/,/^\[/ s/^enable = false/enable = true/' ~/.fetchd/config/app.toml
  sed -i '/^\[api\]$/,/^\[/ s/^swagger = false/swagger = true/' ~/.fetchd/config/app.toml
  fetchd start
  ```

- Execute:

  ```bash
  docker run -it --rm --entrypoint /scripts/<ENTRYPOINT-SCRIPT-NAME> -p 9090:9090 -p 1317:1317 --mount type=bind,source=<FULL-PATH-TO-ENTRYPOINT-SCRIPT>,destination=/scripts/ <FETCH-IMAGE-TAG>
  ```

where

- `<ENTRYPOINT-SCRIPT-NAME>` is the name of the entrypoint script (e.g.`fetchd_initialise.sh`)
- `<PATH-TO-ENTRYPOINT-SCRIPT>` is the path to the directory you placed the script (e.g.`~/fetchd_docker/`),
- `<FETCH-IMAGE-TAG>` is the tag of the FetchD docker image you want to run (e.g. `fetchai/fetchd:0.10.0` for Dorado)
