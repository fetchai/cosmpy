# Release History

## 0.5.1

* dev dependency grpcio-tools updated to 1.47.0
* dev dependency protobuf pinned to 3.19.4
* cosmos sdk proto files regenerated with newer grpcio tool

## 0.5.0

* add BLS support
* add ability to create wallet from mnemonic or unsafe seed
* add integration tests
* LedgerContract switches path to optional
* add address prefix to wallet
* Add fallback hashlib for Ubuntu 22.04 LTS

* fix: send funds in contract methods 
* fix integration tests
* fix: improve support for other chains

* staking auto-compounder use-case
* oracle example use-case
* stake optimizer use-case
* top-up wallet use-case

* update documentation

## 0.4.1

* fix: mainnet chain_id and fee (#141)

## 0.4.0

* fixes for rest api support (#138)
* configuration updates for dorado (#135)
* dorado updates (#115)
* upgrade module (#130)
* add docs preview (#136)
* ibc module (#118)
* tendermint module (#128)

## 0.3.1

* Aerial High Level API by @ejfitzgerald in #96
* Aerial: Initial offline table based gas strategy by @ejfitzgerald in #107
* gov module queries support by @solarw in #91
* Aerial: Simulation based Gas estimation by @ejfitzgerald in #108
* added darglint to make lint command by @solarw in #109
* unused darglint config removed from the setup.cfg by @solarw in #111
* chores: update protos, fix Makefile by @daeMOn63 in #113
* add slashing module API by @solarw in #116
* added evidence module API by @solarw in #117
* fix staking tests by @daeMOn63 in #119
* feat: add params rest client by @daeMOn63 in #120
* Add distribution module by @Galadrin in #92
* Mint module by @solarw in #122
* Initial documentation using MkDocs by @5A11 in #123
* Basic staking support by @ejfitzgerald in #125
* Minor docs edit by @5A11 in #129
* Feature/release 0.3.0 by @5A11 in #131
* Release 0.3.0 by @5A11 in #132

## 0.3.0 (2022-03-30)

* Introduced `Aerial` high-level API.
  * Groundwork for a strategy engine for choosing tx gas fees
  * Simulation-based gas estimation
  * Support for queries, sending tokens, wallets, basic smart contract interactions
  * Support for staking-related logic

* Added documentation using MkDocs
  
* Added low-level support for Cosmos SDK's `gov` module
* Added low-level support for Cosmos SDK's `distribution` module
* Added low-level support for Cosmos SDK's `mint` module

* Added low-level support for Cosmos SDK's `slashing` module
* Added low-level support for Cosmos SDK's `evidence` module

* Improvement to linters (added `darglint` to `make lint`). Resolved `darglint` complains.

* Various fixes and cleanups

## 0.2.0 (2022-02-09)

* Fixed some REST api bugs

## 0.2.0-rc1 (2022-02-03)

* Added support for a Capricorn version of FetchD network

## 0.1.4 (2021-08-25)

* Dependencies refactored and some dependencies will install only with --dev parameter

## 0.1.3 (2021-08-24)

* Lowered required version of grpcio to 1.32.0 or greater

## 0.1.2 (2021-08-23)

* First public release
