# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

import time
from dataclasses import dataclass

import requests

from tests.integration.utils.container import Container


@dataclass
class ChainStatus:
    rest_endpoint: str
    grpc_endpoint: str
    chain_id: str
    latest_block_height: int
    latest_block_time: str

    def is_started(self):
        return self.latest_block_height > 0


class StatusError(Exception):
    pass


class Chain:
    def __init__(self, container: Container):
        self._test_container = container

    def start(self, timeout_seconds=15) -> ChainStatus:
        if self.is_started():
            return

        self._test_container.start()

        sleep_duration = 0.5
        elapsed = 0
        while elapsed < timeout_seconds:
            if self._test_container.is_exited():
                raise StatusError(
                    f"container exited.\nLogs:\n{self._test_container.logs()}"
                )

            try:

                status = self.status()
                if status.is_started():
                    return status
            except StatusError:
                pass

            time.sleep(sleep_duration)
            elapsed += sleep_duration

        raise StatusError("failed to start test network")

    def is_started(self):
        try:
            return self.status().is_started()
        except StatusError:
            return False

    def stop(self):
        if not self.is_started():
            return
        self._test_container.stop()

    def status(self):
        ip = self._test_container.ip()
        if ip is None or ip == "":
            raise StatusError("container does not have IP")
        try:
            r = requests.get(f"http://{ip}:26657/status")
        except Exception as e:
            raise StatusError(f"failed to request chain status from rpc: {str(e)}")
        if r.status_code != 200:
            raise StatusError(
                f"invalid response from status page: {r.status_code} {r.json()}"
            )

        status = r.json()["result"]
        return ChainStatus(
            rest_endpoint=f"rest+http://{ip}:1317/",
            grpc_endpoint=f"grpc+http://{ip}:9090",
            chain_id=status["node_info"]["network"],
            latest_block_height=int(status["sync_info"]["latest_block_height"]),
            latest_block_time=status["sync_info"]["latest_block_time"],
        )
