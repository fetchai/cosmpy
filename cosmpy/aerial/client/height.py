from __future__ import annotations

import types
from dataclasses import dataclass
from typing import Any, Optional, Sequence, Tuple


# gRPC metadata type
Metadata = Sequence[Tuple[str, str]]


def _merge_metadata(base: Metadata, extra: Optional[Metadata]) -> Metadata:
    """
    Merge gRPC metadata tuples.
    Existing metadata is preserved; height metadata is prepended.
    """
    return tuple(base) + tuple(extra or ())


@dataclass(frozen=True)
class GrpcStubWithHeight:
    """
    Wraps a generated gRPC stub (BankGrpcClient, StakingGrpcClient, etc.)
    and injects x-cosmos-block-height metadata into every RPC call.
    """

    stub: Any
    height: int

    def __getattr__(self, name: str) -> Any:
        target = getattr(self.stub, name)

        # Non-callable attributes are passed through unchanged
        if not callable(target):
            return target

        def call(*args: Any, **kwargs: Any) -> Any:
            # Inject Cosmos SDK block height via gRPC metadata
            height_md: Metadata = (("x-cosmos-block-height", str(self.height)),)
            kwargs["metadata"] = _merge_metadata(height_md, kwargs.get("metadata"))
            return target(*args, **kwargs)

        return call


@dataclass(frozen=True)
class LedgerClientAtHeightView:
    """
    A height-scoped view of LedgerClient.

    - All gRPC stub calls automatically receive height metadata
    - High-level LedgerClient methods also work, because methods are
      rebound so that `self` refers to this view
    """

    client: Any
    height: int

    # Names of attributes on LedgerClient that are gRPC stubs
    _GRPC_STUB_ATTRS = {
        "wasm",
        "auth",
        "txs",
        "bank",
        "staking",
        "distribution",
        "params",
        "consensus",
        "tendermint",
    }

    def __getattr__(self, name: str) -> Any:
        """
        Attribute resolution order:

        1) gRPC stubs (bank, staking, wasm, ...)
           -> return a wrapped stub that injects height metadata

        2) LedgerClient methods
           -> rebind the method to this view so `self.bank` goes through the wrapper

        3) Everything else
           -> passthrough to the original client
        """
        obj = getattr(self.client, name)

        # 1) Wrap gRPC stubs
        if name in self._GRPC_STUB_ATTRS:
            return GrpcStubWithHeight(obj, self.height)

        # 2) Rebind LedgerClient methods to this view
        #    This ensures that inside the method, `self.bank`
        #    resolves via this view and not the original client
        if callable(obj) and hasattr(obj, "__func__"):
            return types.MethodType(obj.__func__, self)

        # 3) Fallback: return attribute unchanged
        return obj
