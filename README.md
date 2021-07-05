# PyCosm

A library for interacting with cosmos based networks


# Generate python types form Cosmos-SDK protobuf schema:
## First fetch Cosmos-SDK protobuf schema files (ONE-OFF step):
>NOTE: This is normally one-off step. In the case, that completely new version of Cosmos-SDK is required (see the
`COSMOS_SDK_VERSION` variable in the [Makefile](#Makefile])), it might be
better to force it to re-fetch manually again - please run following command in that case:

```shell
make fetch_proto_schema_source
```

>NOTE: Please note that source protobuf schema files are intentionally **NOT** committed in this repo, they are 
> fetched on demand and stored as **local** files.


## Generate python types:
Run the following command:
```shell
make generate_proto_types
```
>NOTE: The Cosmos-SDK is intentionally not made part of this repository 
> (e.g. via `git submodule ...`, or `git subtree ...`, or by-value(
> trivial copy).
> The reason being to minimise filesystem footprint of this repository.
> It is **NOT** necessary to store Cosmos-SDK protobuf schema files in
> this repository, only python types generated out of protobuf schema is
> actually necessary.
> The makefile target id implemented the way, that necessary bits & pieces
> of Cosmos-SDK repository is downloaded on demand (for python types
> generation), but they are **NOT** checked-in to this repository
