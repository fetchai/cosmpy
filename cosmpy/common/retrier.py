import time
from typing import Callable, Type

from cosmpy.common.loggers import get_logger

_logger = get_logger(__name__)


class Retrier:
    """
    Implementation of a ledger service class.
    """

    def __init__(
        self,
        n_retries: int,
        retry_interval: float,
        log_retries: bool = True,
        call_name: str = "execution",
        raise_exception_type: Type[Exception] = Exception,
    ):
        """
        Create new instance of Retrier

        :param n_retries: Number of retry attempts
        :param retry_interval: Length of sleep between retries
        :param log_retries: bool if retries should be logged
        :param call_name: str call name for logging
        :param raise_exception_type: Type of exception to be raised when call fails to execute after multiple attempts
        """

        self.n_retries = n_retries
        self.retry_interval = retry_interval
        self.log_retries = log_retries
        self.call_name = call_name
        self.raise_exception_type = raise_exception_type

    def call_with_retry(
        self,
        call: Callable,
        *args,
        **kwargs,
    ):
        """
        Try to execute call, retry if exception is thrown

        :param call: Callable to be called with args and kwargs
        :param args: Args to be passed to call
        :param kwargs: Kwargs to be passed to call

        :raises raise_exception_type: When retry fails after specified number of attempts

        :return: response returned from call
        """

        last_exception = None
        response = None

        attempt = 0
        while attempt < self.n_retries:
            attempt += 1
            try:
                response = call(*args, **kwargs)
                if response is not None:
                    break
            except Exception as e:  # pylint: disable=W0703
                last_exception = e
                if self.log_retries:
                    _logger.warning(
                        "%s failed, retry in %s seconds: %s",
                        self.call_name,
                        self.retry_interval,
                        e,
                    )
                time.sleep(self.retry_interval)
                continue

        if response is None:
            raise self.raise_exception_type(
                f"{self.call_name} failed after multiple attempts: {last_exception}"
            ) from last_exception

        return response
