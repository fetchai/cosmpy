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

"""Cosmpy aerial module."""


def cast_to_int(value: str, verify_decimal_part: bool = True, base: int = 10) -> int:
    parts = value.split('.')
    len_parts = len(parts)

    if not (0 < len_parts < 3):
        raise ValueError(f'invalid string literal for casting to int with base {base}: "{value}"')

    integral_part_str = parts[0]

    if integral_part_str == '':
        return 0

    if verify_decimal_part and len_parts > 1:
        # Verify convertibility of the number *behind* the decimal point
        _ = int(parts[1], base)

    return int(integral_part_str, base)
