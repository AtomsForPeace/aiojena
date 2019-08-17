#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: client.py

from typing import Dict
from rdflib import URIRef
from aiosparql.client import SPARQLClient
from aiojena.exceptions import UnknownType
from aiojena.xml_types import string_type, integer_type


def add_type(value, xml_type) -> str:
    return '"' + value + '"^^' + xml_type.n3()


def parse_query(query: str, params: Dict) -> str:
    if not params:
        return query
    _params = {}
    for key, value in params.items():
        if isinstance(value, URIRef):
            _params[key] = value.n3()
        elif isinstance(value, str):
            if value.startswith('?'):
                _params[key] = value
            else:
                _params[key] = add_type(value, string_type)
        elif isinstance(value, int):
            _params[key] = add_type(str(value), integer_type)
        else:
            UnknownType('Received unknown type f{value}')
    return query.format(**_params)


def parse_results(results: Dict):
    bindings = results['results']['bindings']
    parsed = []
    for variable_dict in bindings:
        _results = {}
        for variable_name, variable_info in variable_dict.items():
            if variable_info['type'] == 'literal':
                if URIRef(variable_info['datatype']) == string_type:
                    _results[variable_name] = variable_info['value']
                elif URIRef(variable_info['datatype']) == integer_type:
                    _results[variable_name] = int(variable_info['value'])
            elif variable_info['type'] == 'uri':
                _results[variable_name] = URIRef(
                    value=variable_info['value']
                ).n3()
            else:
                raise UnknownType(variable_info['type'])
        parsed.append(_results)
    return parsed


class JenaClient(SPARQLClient):
    def __init__(self, endpoint, *args, **kwargs):
        super().__init__(endpoint, *args, **kwargs)

    async def query(self, query: str, params: Dict = {}, *args, **kwargs):
        parsed_query_string = parse_query(query, params)
        unparsed = await super().query(parsed_query_string, *args, **kwargs)
        parsed_results = parse_results(results=unparsed)
        return parsed_results

    async def update(self, query: str, params: Dict = {}, *args, **kwargs):
        parsed_query_string = parse_query(query, params)
        await super().update(parsed_query_string, *args, **kwargs)
