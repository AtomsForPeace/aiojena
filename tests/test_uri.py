#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: test_uri.py

import pytest
from aiojena.uri import URI, parse_uri_value


@pytest.mark.asyncio
async def test_uri(jena_client, truncate_jena):
    test_uri_string = 'rdfs:label'
    test_uri = URI(test_uri_string)
    insert_query = """
    INSERT DATA {{
      <http://test.com>     {test_uri}      'Label'
    }}
    """.format(test_uri=test_uri)
    await jena_client.update(insert_query)

    select_query = """
    SELECT ?uri
    WHERE {
      <http://test.com>     ?uri            'Label'
    }
    """
    results = await jena_client.query(select_query)
    assert len(results) == 1
    assert results[0]['uri'] == test_uri


def test_parse_uri_value():
    rdfs_label = 'rdfs:label'
    rdfs_label_url = '<http://www.w3.org/2000/01/rdf-schema#label>'
    assert parse_uri_value(value=rdfs_label) == rdfs_label_url
    assert parse_uri_value(value=rdfs_label_url) == rdfs_label_url
