NODE_CONFIG_PRESETS = {
    "stargate": dict(
        chain_id="stargateworld-3",
        node_address="https://rest-stargateworld.fetch.ai:443",
        faucet_url="https://faucet-stargateworld.t-v2-london-c.fetch-ai.com",
        prefix="fetch",
        denom="atestfet",
    ),
    "local_net": dict(
        chain_id="testing",
        node_address="http://127.0.0.1:1317",
        prefix="fetch",
        denom="stake",
    ),
}
