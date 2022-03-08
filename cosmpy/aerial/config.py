from dataclasses import dataclass


class NetworkConfigError(RuntimeError):
    pass


URL_PREFIXES = (
    "grpc+https",
    "grpc+http",
    "rest-https",
    "rest-http",
)


@dataclass
class NetworkConfig:
    chain_id: str
    fee_minimum_gas_price: int
    fee_denomination: str
    url: str

    def validate(self):
        if self.chain_id == "":
            raise NetworkConfigError("Chain id must be set")
        if self.url == "":
            raise NetworkConfigError("URL must be set")
        if not any(map(lambda x: self.url.startswith(x), URL_PREFIXES)):
            prefix_list = ", ".join(map(lambda x: f'"{x}"', URL_PREFIXES))
            raise NetworkConfigError(
                f"URL must start with one of the following prefixes: {prefix_list}"
            )

    @classmethod
    def capricorn_testnet(cls) -> "NetworkConfig":
        return NetworkConfig(
            chain_id="capricorn-1",
            url="grpc+https://grpc-capricorn.fetch.ai",
            fee_minimum_gas_price=5000000000,
            fee_denomination="atestfet",
        )

    @classmethod
    def latest_stable_testnet(cls) -> "NetworkConfig":
        return cls.capricorn_testnet()
