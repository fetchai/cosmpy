from abc import ABC, abstractmethod
import cosmos.tx.v1beta1.service_pb2 as svc


class RPCInterface(ABC):
    @abstractmethod
    def Simulate(self, request: svc.SimulateRequest) -> svc.SimulateResponse:
        """Simulate simulates executing a transaction for estimating gas usage."""
        pass

    @abstractmethod
    def GetTx(self, request: svc.GetTxRequest) -> svc.GetTxResponse:
        """GetTx fetches a tx by hash."""
        pass

    @abstractmethod
    def BroadcastTx(self, request: svc.BroadcastTxRequest) -> svc.BroadcastTxResponse:
        """BroadcastTx broadcast transaction."""
        pass

    @abstractmethod
    def GetTxsEvent(self, request: svc.GetTxsEventRequest) -> svc.GetTxsEventResponse:
        """GetTxsEvent fetches txs by event."""
        pass
