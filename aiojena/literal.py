#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: literal.py

from aiojena.xml_types import string_type, integer_type


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            return '"' + self.value + string_type
        if isinstance(self.value, int):
            return '"' + str(self.value) + integer_type

    def __eq__(self, other):
        return str(self.value) == str(other)
