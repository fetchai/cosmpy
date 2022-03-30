# Release History

## 0.3.0 (2022-03-30)

- Introduced `Aerial` high-level API.
  - Groundwork for a strategy engine for choosing tx gas fees
  - Simulation-based gas estimation
  - Support for queries, sending tokens, wallets, basic smart contract interactions
  - Support for staking-related logic

- Added documentation using MkDocs
  
- Added low-level support for Cosmos SDK's `gov` module
- Added low-level support for Cosmos SDK's `distribution` module
- Added low-level support for Cosmos SDK's `mint` module
- Added low-level support for Cosmos SDK's `slashing` module
- Added low-level support for Cosmos SDK's `evidence` module

- Improvement to linters (added `darglint` to `make lint`). Resolved `darglint` complains.

- Various fixes and cleanups

## 0.2.0 (2022-02-09)

- Fixed some REST api bugs

## 0.2.0-rc1 (2022-02-03)

- Added support for a Capricorn version of FetchD network

## 0.1.4 (2021-08-25)

- Dependencies refactored and some dependencies will install only with --dev parameter

## 0.1.3 (2021-08-24)

- Lowered required version of grpcio to 1.32.0 or greater

## 0.1.2 (2021-08-23)

- First public release
