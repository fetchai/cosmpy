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

"""Module with base test cases for integration tests."""

from unittest import TestCase

import pytest  # pylint: disable=import-error
from docker.errors import NotFound  # pylint: disable=import-error

from tests.integration.generic.fetchd_client import FetchdDockerImage


@pytest.mark.integtest
class FetchdTestCase(TestCase):
    """Base test case for Fetchd node."""

    @classmethod
    def setUpClass(cls):
        """Set up Fetchd node for testing."""
        cls.client = FetchdDockerImage()
        cls._try_launch_image()

    @classmethod
    def _try_launch_image(cls):
        """Try to launch image and retry if first run was not successful."""
        try:
            cls.client.launch_image()
        except NotFound:
            # After machine reboot first run is not successful with NotFound exception.
            # So if it happens we run it the second time and it is successful.
            cls.client.launch_image()

    @classmethod
    def tearDownClass(cls):
        """Teardown the Fetchd node."""
        cls.client.stop_image()
