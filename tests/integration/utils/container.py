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

import os

import docker


class Container:
    """Manage a docker container running a single node testnet for integration tests."""

    def __init__(self):
        self._docker_client = docker.from_env()
        self._image_name = "cosmpy-testnode"
        self._container = None

    def _build_image(self):
        self._docker_client.images.build(
            path=os.path.dirname(os.path.realpath(__file__)),
            tag=self._image_name,
        )

    def start(self):
        self._build_image()
        if self._container is None:
            fetchd_home_volume = self._docker_client.volumes.create()
            self._container = self._docker_client.containers.run(
                self._image_name,
                detach=True,
                volumes=[f"{fetchd_home_volume.name}:/root/.fetchd"],
            )
        # somehow self._container attrs are not set by run() call,
        # so we need to refetch the container from the docker daemon to
        # have attrs like the IP address available
        self._container = self._docker_client.containers.get(self._container.id)

    def is_exited(self) -> bool:
        if self._container is None:
            return True

        return self._docker_client.containers.get(self._container.id).status == "exited"

    def logs(self) -> str:
        if self._container is None:
            return ""

        return self._container.logs().decode("utf-8")

    def ip(self):
        if self._container is None:
            return None

        return self._container.attrs["NetworkSettings"]["IPAddress"]

    def stop(self):
        if self._container is None:
            return

        self._container.stop()
        self._container.remove(v=True, force=True)

    def restart(self):
        if self._container is None:
            self.start()
            return

        self._container.restart()
