#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: test_literal.py

import pytest
from aiojena.literal import Literal


@pytest.mark.asyncio
async def test_string_literal(jena_client, truncate_jena):
    test_string = 'String'
    test_literal = Literal(test_string)
    insert_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    INSERT DATA {{
      <http://test.com>     rdfs:label      {test_literal}
    }}
    """.format(test_literal=test_literal)
    await jena_client.update(insert_query)

    select_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?string
    WHERE {
      <http://test.com>     rdfs:label      ?string
    }
    """
    results = await jena_client.query(select_query)
    assert len(results) == 1
    assert results[0]['string'] == test_string


@pytest.mark.asyncio
async def test_int_literal(jena_client, truncate_jena):
    test_integer = 1
    test_literal = Literal(test_integer)
    query_string = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    INSERT DATA {{
      <http://test.com>     rdfs:label      {test_literal}
    }}
    """.format(test_literal=test_literal)
    await jena_client.update(query_string)

    select_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?integer
    WHERE {
      <http://test.com>     rdfs:label      ?integer
    }
    """
    results = await jena_client.query(select_query)
    assert len(results) == 1
    assert results[0]['integer'] == test_integer
