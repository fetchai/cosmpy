class QueryError(RuntimeError):
    pass


class NotFoundError(QueryError):
    pass


class QueryTimeoutError(QueryError):
    pass


class BroadcastError(RuntimeError):
    def __init__(self, tx_hash: str, message: str):
        super().__init__(message)
        self.tx_hash = tx_hash


class OutOfGasError(BroadcastError):
    def __init__(self, tx_hash: str, gas_wanted: int, gas_used: int):
        self.gas_wanted = gas_wanted
        self.gas_used = gas_used
        super().__init__(
            tx_hash, f"Out of Gas (wanted: {self.gas_wanted}, used: {self.gas_used})"
        )


class InsufficientFeesError(BroadcastError):
    def __init__(self, tx_hash: str, minimum_required_fee: str):
        self.minimum_required_fee = minimum_required_fee
        super().__init__(
            tx_hash,
            f"Insufficient Fees (minimum required: {self.minimum_required_fee})",
        )
