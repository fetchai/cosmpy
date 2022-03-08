import re
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse


class Protocol(Enum):
    GRPC = 1
    REST = 2


@dataclass
class ParsedUrl:
    protocol: Protocol
    secure: bool
    hostname: str
    port: int

    @property
    def host_and_port(self) -> str:
        return f"{self.hostname}:{self.port}"

    @property
    def rest_url(self) -> str:
        assert self.protocol == Protocol.REST
        if self.secure:
            prefix = "https"
            default_port = 443
        else:
            prefix = "http"
            default_port = 80

        url = f"{prefix}://{self.hostname}"
        if self.port != default_port:
            url += f":{self.port}"
        return url


def parse_url(url: str) -> ParsedUrl:
    result = urlparse(url)
    if result.scheme == "grpc+https":
        protocol = Protocol.GRPC
        secure = True
        default_port = 443
    elif result.scheme == "grpc+http":
        protocol = Protocol.GRPC
        secure = False
        default_port = 80
    elif result.scheme == "rest+https":
        protocol = Protocol.REST
        secure = True
        default_port = 443
    elif result.scheme == "rest+http":
        protocol = Protocol.REST
        secure = False
        default_port = 80
    else:
        raise RuntimeError(f"Unsupported url scheme: {result.scheme}")

    match = re.match(r"^(.+?)(?::(\d+))?$", result.netloc)
    if match is None:
        raise RuntimeError(f"Unable to parse netloc: {result.netloc}")

    # hostname = str(match.group(1))
    # port = int(match.group(2))
    hostname = str(match.group(1))
    port = default_port if match.group(2) is None else int(match.group(2))

    return ParsedUrl(protocol=protocol, secure=secure, hostname=hostname, port=port)
