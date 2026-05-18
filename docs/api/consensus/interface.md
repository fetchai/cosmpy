<a id="cosmpy.consensus.interface"></a>

# cosmpy.consensus.interface

Interface for the Consensus functionality of CosmosSDK.

<a id="cosmpy.consensus.interface.Params"></a>

## Params Objects

```python
class Params(ABC)
```

Params abstract class.

<a id="cosmpy.consensus.interface.Params.Params"></a>

#### Params

```python
@abstractmethod
def Params(request: QueryParamsRequest) -> QueryParamsResponse
```

Params queries a specific Cosmos SDK parameter.

**Arguments**:

- `request`: QueryParamsRequest

**Returns**:

QueryParamsResponse

