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

import os
import re
import shutil
import subprocess  # nosec
import tempfile
import time

import docker  # pylint: disable=import-error
import requests


class FetchdClient:
    """Class to operate Fetchd node with Docker engine."""

    MINIMUM_DOCKER_VERSION = (19, 0, 0)
    ENDPOINT = "http://127.0.0.1:1317"
    IMG_TAG = "fetchai/fetchd:0.8.4"
    ENTRYPOINT_FILENAME = "entry.sh"
    MOUNT_PATH = "/mnt"
    PORTS = {9090: 9090, 1317: 1317, 26657: 26657}
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
        """Initialize Docker and Fetchd."""
        self.client = docker.from_env()
        # self.client.images.pull(self.IMG_TAG)
        self.container = None

    def launch_image(self, timeout: float = 2.0, max_attempts: int = 10):
        """
        Launch image.

        :return: None
        """
        self.check_skip()
        # self.stop_if_already_running()
        self.create()
        self.container.start()
        print(f"Setting up image {self.IMG_TAG}...")
        success = self.wait(max_attempts, timeout)
        if not success:
            self.container.stop()
            self.container.remove()
            raise RuntimeError(f"{self.IMG_TAG} doesn't work. Exiting...")
        else:
            print("Done!")
            time.sleep(timeout)
            # yield
            # print(f"Stopping the image {self.IMG_TAG}...")
            # self.container.stop()
            # self.container.remove()

    def check_skip(self):
        """Check the 'Docker' CLI tool is in the OS PATH."""
        result = shutil.which("docker")
        if result is None:
            raise RuntimeError("Docker not in the OS Path; skipping the test")

        result = subprocess.run(  # nosec
            ["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise RuntimeError(f"'docker --version' failed with exit code {result.returncode}")

        match = re.search(
            r"Docker version ([0-9]+)\.([0-9]+)\.([0-9]+)",
            result.stdout.decode("utf-8"),
        )
        if match is None:
            raise RuntimeError("cannot read version from the output of 'docker --version'")
        version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        if version < self.MINIMUM_DOCKER_VERSION:
            raise RuntimeError(
                f"expected Docker version to be at least {'.'.join(self.MINIMUM_DOCKER_VERSION)}, found {'.'.join(version)}"
            )

    def stop_if_already_running(self):
        """Stop the running images with the same tag, if any."""
        client = docker.from_env()
        for container in client.containers.list():
            if self.IMG_TAG in container.image.tags:
                print(f"Stopping image {self.IMG_TAG}...")
                container.stop()

    def _make_entrypoint(self, dirpath):
        """
        Make an entrypoint file for Fetchd container.

        :param dirpath: str target directory path.
        """
        path = os.path.join(dirpath, self.ENTRYPOINT_FILENAME)
        with open(path, "w") as f:
            f.writelines(line + "\n" for line in self.ENTRYPOINT_LINES)
        os.chmod(path, 300)  # nosec

    def create(self):
        """Run Fetchd node in Docker container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_entrypoint(tmpdir)
            volumes = {tmpdir: {"bind": self.MOUNT_PATH, "mode": "rw"}}
            entrypoint = os.path.join(self.MOUNT_PATH, self.ENTRYPOINT_FILENAME)
            self.container = self.client.containers.run(
                self.IMG_TAG,
                detach=True,
                volumes=volumes,
                entrypoint=str(entrypoint),
                auto_remove=True,
                ports=self.PORTS,
            )

    def stop(self):
        """Stop running Docker container with Fetchd node."""
        if self.container is None:
            raise RuntimeError("Fetchd node is not running.")
        print(f"Stopping the image {self.IMG_TAG}...")
        self.container.stop()
        self.container.remove()

    def wait(self, max_attempts: int = 15, sleep_rate: float = 1.0) -> bool:
        """Wait until the image is up."""
        # request = dict(jsonrpc=2.0, method="web3_clientVersion", params=[], id=1)
        for i in range(max_attempts):
            try:
                response = requests.get(f"{self.ENDPOINT}")
                if response.status_code != 200:
                    raise RuntimeError("")
                return True
            except Exception as e:
                import pdb;pdb.set_trace()
                print(f"Attempt {i} failed. Retrying in {sleep_rate} seconds...")
                time.sleep(sleep_rate)
        return False
