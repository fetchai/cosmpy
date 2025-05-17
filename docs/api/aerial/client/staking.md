<a id="cosmpy.aerial.client.staking"></a>

# cosmpy.aerial.client.staking

Staking functionality.

<a id="cosmpy.aerial.client.staking.ValidatorStatus"></a>

## ValidatorStatus Objects

```python
class ValidatorStatus(Enum)
```

Validator status.

<a id="cosmpy.aerial.client.staking.ValidatorStatus.from_proto"></a>

#### from`_`proto

```python
@classmethod
def from_proto(cls, value: int) -> "ValidatorStatus"
```

Get the validator status from proto.

**Arguments**:

- `value`: value

**Raises**:

- `RuntimeError`: Unable to decode validator status

**Returns**:

Validator status

<a id="cosmpy.aerial.client.staking.StakingPosition"></a>

## StakingPosition Objects

```python
@dataclass
class StakingPosition()
```

Staking positions.

<a id="cosmpy.aerial.client.staking.UnbondingPositions"></a>

## UnbondingPositions Objects

```python
@dataclass
class UnbondingPositions()
```

Unbonding positions.

<a id="cosmpy.aerial.client.staking.Validator"></a>

## Validator Objects

```python
@dataclass
class Validator()
```

Validator.

<a id="cosmpy.aerial.client.staking.StakingSummary"></a>

## StakingSummary Objects

```python
@dataclass
class StakingSummary()
```

Get the staking summary.

<a id="cosmpy.aerial.client.staking.StakingSummary.total_staked"></a>

#### total`_`staked

```python
@property
def total_staked() -> int
```

Get the total staked amount.

<a id="cosmpy.aerial.client.staking.StakingSummary.total_rewards"></a>

#### total`_`rewards

```python
@property
def total_rewards() -> int
```

Get the total rewards.

<a id="cosmpy.aerial.client.staking.StakingSummary.total_unbonding"></a>

#### total`_`unbonding

```python
@property
def total_unbonding() -> int
```

total unbonding.

<a id="cosmpy.aerial.client.staking.create_delegate_msg"></a>

#### create`_`delegate`_`msg

```python
def create_delegate_msg(delegator: Address, validator: Address, amount: int,
                        denom: str) -> MsgDelegate
```

Create delegate message.

**Arguments**:

- `delegator`: delegator
- `validator`: validator
- `amount`: amount
- `denom`: denom

**Returns**:

Delegate message

<a id="cosmpy.aerial.client.staking.create_redelegate_msg"></a>

#### create`_`redelegate`_`msg

```python
def create_redelegate_msg(delegator_address: Address,
                          validator_src_address: Address,
                          validator_dst_address: Address, amount: int,
                          denom: str) -> MsgBeginRedelegate
```

Create redelegate message.

**Arguments**:

- `delegator_address`: delegator address
- `validator_src_address`: source validation address
- `validator_dst_address`: destination validation address
- `amount`: amount
- `denom`: denom

**Returns**:

Redelegate message

<a id="cosmpy.aerial.client.staking.create_undelegate_msg"></a>

#### create`_`undelegate`_`msg

```python
def create_undelegate_msg(delegator_address: Address,
                          validator_address: Address, amount: int,
                          denom: str) -> MsgUndelegate
```

Create undelegate message.

**Arguments**:

- `delegator_address`: delegator address
- `validator_address`: validator address
- `amount`: amount
- `denom`: denom

**Returns**:

Undelegate message

