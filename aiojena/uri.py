#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: uri.py


class URI:
    def __init__(self, value):
        self.value = parse_uri_value(value=value)

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return str(self.value) == str(other)


def parse_uri_value(value: str):
    prefix_conversions = {
        'rdfs:': 'http://www.w3.org/2000/01/rdf-schema#'
    }
    for prefix in prefix_conversions:
        if prefix in value:
            return \
                '<' + value.replace(prefix, prefix_conversions[prefix]) + '>'
        elif value.startswith('http'):
            return '<' + value + '>'
    return value
