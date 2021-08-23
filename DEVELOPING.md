## Generate python types from Cosmos-SDK protobuf schemas

### Fetch Cosmos-SDK protobuf schema files
>NOTE: When updating to a different version of the Cosmos SDK (see the version currently used under `COSMOS_SDK_VERSION` in [Makefile](#Makefile])), you will need to perform this step once to fetch the relevant protobuf schema files:

```bash
make fetch_proto_schema_source
```

>NOTE: For this library to be functional, only the python types generated from protobuf schemas are required, not the schema files themselves.
> The schema files are fetched on-demand only to enable the generation of python types.
> Therefore, the schema files are intentionally stored as **local** files and are **NOT** checked in to this repository to minimise its filesystem footprint.

### Generate python types
```bash
make generate_proto_types
```

## Setup a local Stargate node

### Preliminaries

You require Go version 15.0 or higher for your platform (see <a href="https://golang.org/doc/install" target="_blank">here</a>)

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

## Examples

### Preliminaries

- Install the package from source:
  ```bash
  pipenv install
  ```

- or in development mode:
  ```bash
  pipenv install --dev
  ```

- Launch a virtual environment
  ```bash
  pipenv shell
  ```

### Run Examples

- Query balance example using REST api
  ```bash
  python src/examples/query_balance_rest_example.py
  ```

- Send funds transaction example
  - Using gRPC
    ```bash
    python src/examples/tx_send_grpc_example.py
    ```
  - Using REST api
    ```bash
    python src/examples/tx_send_rest_example.py
    ```

- Contract deployment and interaction example
  - Using gRPC
    ```bash
    python src/examples/contract_interaction_grpc_example.py
    ```
  - Using REST api
    ```bash
    python src/examples/contract_interaction_rest_example.py
    ```

- Native tokens atomic swap example 
  - Using gRPC
    ```bash
    python src/examples/tx_native_tokens_atomic_swap_grpc_example.py
    ```
  - Using REST api
    ```bash
    python src/examples/tx_native_tokens_atomic_swap_rest_example.py
    ```

- Atomic swap using ERC1155 contract example
  - Using gRPC
    ```bash
    python src/examples/atomic_swap_contract_grpc_example.py
    ```
  - Using REST api
    ```bash
    python src/examples/atomic_swap_contract_rest_example.py
    ```
