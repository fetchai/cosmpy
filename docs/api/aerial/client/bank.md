<a id="c4epy.aerial.client.bank"></a>

# c4epy.aerial.client.bank

Bank send message.

<a id="c4epy.aerial.client.bank.create_bank_send_msg"></a>

#### create`_`bank`_`send`_`msg

```python
def create_bank_send_msg(from_address: Address, to_address: Address,
                         amount: int, denom: str) -> MsgSend
```

Create bank send message.

**Arguments**:

- `from_address`: from address
- `to_address`: to address
- `amount`: amount
- `denom`: denom

**Returns**:

bank send message

