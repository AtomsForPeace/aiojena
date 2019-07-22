#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: literal.py

string_type = '<http://www.w3.org/2001/XMLSchema#string>'


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            return '"' + self.value + '"'
        if isinstance(self.value, int):
            return '"' + str(self.value) + \
                '"^^<http://www.w3.org/2001/XMLSchema:integer>'

    def __eq__(self, other):
        return str(self.value) == str(other)
