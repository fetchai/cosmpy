import requests


URLS = {
    # Validators queries all validators that match the given status.
    "Validators": "/validators",
    # Validator queries validator info for given validator address.
    "Validator": "/validators/{validator_addr}",
    # ValidatorDelegations queries delegate info for given validator.
    "ValidatorDelegations": "/validators/{validator_addr}/delegations",
    # ValidatorUnbondingDelegations queries unbonding delegations of a validator.
    "ValidatorUnbondingDelegations": "/validators/{validator_addr}/unbonding_delegations",
    # Delegation queries delegate info for given validator delegator pair.
    "Delegation": "/validators/{validator_addr}/delegations/{delegator_addr}",
    # UnbondingDelegation queries unbonding info for given validator delegator pair.
    "UnbondingDelegation": "/validators/{validator_addr}/delegations/{delegator_addr}/unbonding_delegation",
    # DelegatorDelegations queries all delegations of a given delegator address.
    "DelegatorDelegations": "/delegations/{delegator_addr}",
    # DelegatorUnbondingDelegations queries all unbonding delegations of a given delegator address.
    "DelegatorUnbondingDelegations": "/delegators/{delegator_addr}/unbonding_delegations",
    # Redelegations queries redelegations of given address.
    "Redelegations": "/delegators/{delegator_addr}/redelegations",
    # DelegatorValidators queries all validators info for given delegator address.
    "DelegatorValidators": "/delegators/{delegator_addr}/validators",
    # DelegatorValidator queries validator info for given delegator validator pair.
    "DelegatorValidator": "/delegators/{delegator_addr}/validators/{validator_addr}",
    # HistoricalInfo queries the historical info for given height.
    "HistoricalInfo": "/historical_info/{height}",
    # Pool queries the pool info.
    "Pool": "/pool",
    # Parameters queries the staking parameters.
    "Params": "/params",
}

API_URL = "http://127.0.0.1:1317"
STAKING_URL = "/cosmos/staking/v1beta1"


def api_get(url):
    response = requests.get(url=url)
    assert response.status_code == 200
    return response.json()


def staking_get(url):
    return api_get(f"{API_URL}{STAKING_URL}{url}")


def query_get(url, **kwargs):
    if kwargs:
        url = url.format(**kwargs)
    return staking_get(url)


# wrappers


def get_validators():
    return query_get(URLS["Validators"])


def get_validator(validator_addr):
    return query_get(
        URLS["Validator"],
        validator_addr=validator_addr,
    )


def get_validator_delegations(validator_addr):
    return query_get(
        URLS["ValidatorDelegations"],
        validator_addr=validator_addr,
    )


def get_validator_unbonding_delegations(validator_addr):
    return query_get(
        URLS["ValidatorUnbondingDelegations"],
        validator_addr=validator_addr,
    )


def get_delegation(validator_addr, delegator_addr):
    return query_get(
        url=URLS["Delegation"],
        validator_addr=validator_addr,
        delegator_addr=delegator_addr,
    )


def get_unbonding_delegation(validator_addr, delegator_addr):
    return query_get(
        url=URLS["UnbondingDelegation"],
        validator_addr=validator_addr,
        delegator_addr=delegator_addr,
    )


def get_delegator_delegations(delegator_addr):
    return query_get(
        URLS["DelegatorDelegations"],
        delegator_addr=delegator_addr,
    )


def get_delegator_unbonding_delegation(delegator_addr):
    return query_get(
        URLS["DelegatorUnbondingDelegations"],
        delegator_addr=delegator_addr,
    )


def get_redelegations(delegator_addr):
    return query_get(
        URLS["Redelegations"],
        delegator_addr=delegator_addr,
    )


def get_delegator_validators(delegator_addr):
    return query_get(
        URLS["DelegatorValidators"],
        delegator_addr=delegator_addr,
    )


def get_delegator_validator(delegator_addr, validator_addr):
    return query_get(
        URLS["DelegatorValidator"],
        delegator_addr=delegator_addr,
        validator_addr=validator_addr,
    )


def get_historical_info(height):
    return query_get(
        URLS["HistoricalInfo"],
        height=height,
    )


def get_pool():
    return query_get(
        url=URLS["Pool"],
    )


def get_params():
    return query_get(
        URLS["Params"],
    )
