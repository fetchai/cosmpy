from abc import ABC, abstractmethod
from cosmwasm.wasm.v1beta1.query_pb2 import (
    QuerySmartContractStateRequest,
    QuerySmartContractStateResponse,
    QueryAllContractStateRequest,
    QueryAllContractStateResponse,
    QueryCodeRequest,
    QueryCodeResponse,
    QueryCodesRequest,
    QueryCodesResponse,
    QueryContractHistoryRequest,
    QueryContractHistoryResponse,
    QueryContractInfoRequest,
    QueryContractInfoResponse,
    QueryContractsByCodeRequest,
    QueryContractsByCodeResponse,
    QueryRawContractStateRequest,
    QueryRawContractStateResponse,
)


class Wasm(ABC):
    @abstractmethod
    def ContractInfo(
        self, request: QueryContractInfoRequest
    ) -> QueryContractInfoResponse:
        """
        Gets the contract meta data

        :param request: QueryContractInfoRequest

        :return: QueryContractInfoResponse
        """
        pass

    @abstractmethod
    def ContractHistory(
        self, request: QueryContractHistoryRequest
    ) -> QueryContractHistoryResponse:
        """
        Gets the contract code history

        :param request: QueryContractHistoryRequest

        :return: QueryContractHistoryResponse
        """
        pass

    @abstractmethod
    def ContractsByCode(
        self, request: QueryContractsByCodeRequest
    ) -> QueryContractsByCodeResponse:
        """
        Lists all smart contracts for a code id

        :param request: QueryContractsByCodeRequest

        :return: QueryContractsByCodeResponse
        """
        pass

    @abstractmethod
    def AllContractState(
        self, request: QueryAllContractStateRequest
    ) -> QueryAllContractStateResponse:
        """
        Gets all raw store data for a single contract

        :param request: QueryAllContractStateRequest

        :return: QueryAllContractStateResponse
        """
        pass

    @abstractmethod
    def RawContractState(
        self, request: QueryRawContractStateRequest
    ) -> QueryRawContractStateResponse:
        """
        Gets single key from the raw store data of a contract

        :param request: QueryRawContractStateRequest

        :return: QueryRawContractStateResponse
        """
        pass

    @abstractmethod
    def SmartContractState(
        self, request: QuerySmartContractStateRequest
    ) -> QuerySmartContractStateResponse:
        """
        Get smart query result from the contract

        :param request: QuerySmartContractStateRequest

        :return: QuerySmartContractStateResponse
        """
        pass

    @abstractmethod
    def Code(self, request: QueryCodeRequest) -> QueryCodeResponse:
        """
        Gets the binary code and metadata for a singe wasm code

        :param request: QueryCodeRequest

        :return: QueryCodeResponse
        """
        pass

    @abstractmethod
    def Codes(self, request: QueryCodesRequest) -> QueryCodesResponse:
        """
        Gets the metadata for all stored wasm codes

        :param request: QueryCodesRequest

        :return: QueryCodesResponse
        """
        pass
