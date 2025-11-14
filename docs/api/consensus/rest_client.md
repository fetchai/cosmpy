<a id="cosmpy.consensus.rest_client"></a>

# cosmpy.consensus.rest`_`client

Implementation of Params interface using REST.

<a id="cosmpy.consensus.rest_client.ConsensusRestClient"></a>

## ConsensusRestClient Objects

```python
class ConsensusRestClient(Params)
```

Consensus REST client.

<a id="cosmpy.consensus.rest_client.ConsensusRestClient.__init__"></a>

#### `__`init`__`

```python
def __init__(rest_api: RestClient) -> None
```

Initialize.

**Arguments**:

- `rest_api`: RestClient api

<a id="cosmpy.consensus.rest_client.ConsensusRestClient.Params"></a>

#### Params

```python
def Params(request: QueryParamsRequest) -> QueryParamsResponse
```

Params queries a specific Cosmos SDK parameter.

**Arguments**:

- `request`: QueryParamsRequest

**Returns**:

QueryParamsResponse

