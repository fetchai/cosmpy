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

"""Module with FetchdClient class for easy usage of Fetchd node with Docker engine."""

import logging
import os
import re
import shutil
import subprocess  # nosec
import tempfile
import time

import docker  # pylint: disable=import-error

from cosmpy.clients.signing_cosmwasm_client import CosmWasmClient
from cosmpy.common.rest_client import RestClient
from tests.integration.generic.config import (
    DENOM,
    REST_ENDPOINT_ADDRESS,
    VALIDATOR_ADDRESS,
)


class FetchdDockerImage:
    """Class to operate Fetchd node with Docker engine."""

    MINIMUM_DOCKER_VERSION = (19, 0, 0)

    IMG_TAG = "fetchai/fetchd:0.9.0-rc4"
    ENTRYPOINT_FILENAME = "entry.sh"
    MOUNT_PATH = "/mnt"
    PORTS = {9090: 9090, 1317: 1317, 26657: 26657}

    DEFAULT_MAX_ATTEMPTS = 10
    DEFAULT_SLEEP_RATE = 2

    # pylint: disable=anomalous-backslash-in-string
    ENTRYPOINT_LINES = (
        "#!/usr/bin/env bash",
        # variables
        "export VALIDATOR_KEY_NAME=validator",
        "export BOB_KEY_NAME=bob",
        'export VALIDATOR_MNEMONIC="erase weekend bid boss knee vintage goat syrup use tumble device album fortune water sweet maple kind degree toss owner crane half useless sleep"',
        'export BOB_MNEMONIC="account snack twist chef razor sing gain birth check identify unable vendor model utility fragile stadium turtle sun sail enemy violin either keep fiction"',
        'export PASSWORD="12345678"',
        "export CHAIN_ID=testing",
        "export DENOM_1=stake",
        "export DENOM_2=atestfet",
        # Add keys
        '( echo "$VALIDATOR_MNEMONIC"; echo "$PASSWORD"; echo "$PASSWORD"; ) |fetchd keys add $VALIDATOR_KEY_NAME --recover',
        '( echo "$BOB_MNEMONIC"; echo "$PASSWORD"; ) |fetchd keys add $BOB_KEY_NAME --recover',
        # Configure node
        "fetchd init --chain-id=$CHAIN_ID $CHAIN_ID",
        'echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $VALIDATOR_KEY_NAME -a) 100000000000000000000000$DENOM_1',
        'echo "$PASSWORD" |fetchd add-genesis-account $(fetchd keys show $BOB_KEY_NAME -a) 100000000000000000000000$DENOM_2',
        'echo "$PASSWORD" |fetchd gentx $VALIDATOR_KEY_NAME 10000000000000000000000$DENOM_1 --chain-id $CHAIN_ID',
        "fetchd collect-gentxs",
        # Enable rest-api
        "sed -i '/^\[api\]$/,/^\[/ s/^enable = false/enable = true/' ~/.fetchd/config/app.toml",  # noqa: W605
        "sed -i '/^\[api\]$/,/^\[/ s/^swagger = false/swagger = true/' ~/.fetchd/config/app.toml",  # noqa: W605
        "fetchd start",
    )

    def __init__(self):
        """Initialize the Fetchd docker image."""
        self.client = docker.from_env()
        self.container = None

    def _check_skip(self):
        """Check the correct version of docker CLI tool is in the OS PATH."""
        result = shutil.which("docker")
        if result is None:
            raise RuntimeError("Docker not in the OS Path; skipping the test")

        result = subprocess.run(  # nosec
            ["docker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"'docker --version' failed with exit code {result.returncode}"
            )

        match = re.search(
            r"Docker version ([0-9]+)\.([0-9]+)\.([0-9]+)",
            result.stdout.decode("utf-8"),
        )
        if match is None:
            raise RuntimeError(
                "cannot read version from the output of 'docker --version'"
            )
        version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        if version < self.MINIMUM_DOCKER_VERSION:
            raise RuntimeError(
                f"expected Docker version to be at least {'.'.join(self.MINIMUM_DOCKER_VERSION)}, found {'.'.join(version)}"
            )

    def _stop_if_already_running(self):
        """Stop the running images with the same tag, if any."""
        for container in self.client.containers.list():
            if self.IMG_TAG in container.image.tags:
                logging.debug("Stopping image %s...", self.IMG_TAG)
                container.stop()

    def _make_entrypoint(self, dirpath):
        """
        Make a temporary entrypoint file to setup and run the test ledger node.

        :param dirpath: str target directory path.
        """
        path = os.path.join(dirpath, self.ENTRYPOINT_FILENAME)
        with open(path, "w") as f:
            f.writelines(line + "\n" for line in self.ENTRYPOINT_LINES)
        os.chmod(path, 300)  # nosec

    def _create(self):
        """Create a Fetchd docker container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_entrypoint(tmpdir)
            volumes = {tmpdir: {"bind": self.MOUNT_PATH, "mode": "rw"}}
            entrypoint = f"{self.MOUNT_PATH}/{self.ENTRYPOINT_FILENAME}"
            self.container = self.client.containers.run(
                self.IMG_TAG,
                detach=True,
                volumes=volumes,
                entrypoint=str(entrypoint),
                auto_remove=True,
                ports=self.PORTS,
            )

    @staticmethod
    def _wait(
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        sleep_rate: float = DEFAULT_SLEEP_RATE,
    ) -> bool:
        """Wait until the image is up."""
        for i in range(max_attempts):
            try:
                time.sleep(sleep_rate)
                rest_client = RestClient(REST_ENDPOINT_ADDRESS)
                client = CosmWasmClient(rest_client)
                res = client.get_balance(VALIDATOR_ADDRESS, DENOM)
                # Make sure that first block is minted
                if int(res.balance.amount) < 1000:
                    raise RuntimeError("The node is not set up yet.")
                return True
            except Exception as e:  # nosec pylint: disable=W0703
                logging.debug(
                    "Attempt %s failed. %s. Retrying in %s seconds...",
                    i,
                    str(e),
                    sleep_rate,
                )
        return False

    def launch_image(
        self,
        timeout: float = DEFAULT_SLEEP_RATE,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ):
        """
        Launch a FetchD docker image.

        :param timeout: number of seconds to wait before checking the image is up.
        :param max_attempts: the maximum number of times to check the image is up.

        :raises RuntimeError: if node is not up and running.
        """
        self._check_skip()
        self._stop_if_already_running()
        self._create()
        self.container.start()
        logging.debug("Setting up image %s...", self.IMG_TAG)
        success = self._wait(max_attempts, timeout)
        if not success:
            self.container.stop()
            self.container.remove()
            raise RuntimeError(f"{self.IMG_TAG} doesn't work. Exiting...")

        logging.debug("Done!")
        time.sleep(timeout)

    def stop_image(self):
        """Stop the FetchD docker image."""
        if self.container is None:
            raise RuntimeError("Fetchd node is not running.")
        logging.debug("Stopping the image %s...", self.IMG_TAG)
        self.container.stop()
        self.container = None
