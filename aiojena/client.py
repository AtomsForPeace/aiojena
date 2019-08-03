#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: client.py

from aiosparql.client import SPARQLClient
from aiojena.literal import Literal
from aiojena.uri import URI


class JenaClient(SPARQLClient):
    def __init__(self, endpoint, *args, **kwargs):
        super().__init__(endpoint, *args, **kwargs)

    async def query(self, query: str, *args, **kwargs):
        unparsed = await super().query(query, *args, **kwargs)
        bindings = unparsed['results']['bindings']
        results = []
        for variable_dict in bindings:
            _results = {}
            for variable_name, variable_info in variable_dict.items():
                if variable_info['type'] == 'literal':
                    _results[variable_name] = Literal(
                        value=variable_info['value']
                    )
                if variable_info['type'] == 'uri':
                    _results[variable_name] = URI(
                        value=variable_info['value']
                    )
            results.append(_results)
        return results
