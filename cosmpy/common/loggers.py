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


""" logging helpers, inspired from https://github.com/fetchai/agents-aea/blob/master/aea/cli/utils/loggers.py """

import logging
import sys
from typing import Dict

import click


class ColorFormatter(logging.Formatter):
    """The default formatter for cli output."""

    colors = {
        "error": dict(fg="red"),
        "exception": dict(fg="red"),
        "critical": dict(fg="red"),
        "debug": dict(fg="blue"),
        "info": dict(fg="green"),
        "warning": dict(fg="yellow"),
    }

    def format(self, record):
        """Format the log message."""
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style(f"{level}: ", **self.colors[level])
                msg = "\n".join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)  # pragma: no cover


def default_logging_config(logger):  # pylint: disable=redefined-outer-name
    """Set up the default handler and formatter on the given logger."""
    default_handler = logging.StreamHandler(stream=sys.stdout)
    default_handler.formatter = ColorFormatter()
    logger.handlers = [default_handler]
    logger.propagate = True
    return logger


_loggers: Dict = {}


def get_logger(name, name_length=1):
    """Get logger by name."""
    global _loggers  # pylint: disable=W0603, W0602
    splitted = name.split(".")
    logger_name = ".".join(splitted[-name_length:])
    logger = logging.getLogger(logger_name)
    logger = default_logging_config(logger)
    _loggers[logger_name] = logger
    return logger
