#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: test_literal.py

from rdflib import URIRef
import pytest


@pytest.mark.asyncio
async def test_string_literal(
    jena_client, truncate_jena, simple_insert, simple_select_object
):
    test_subject = URIRef('http://test.com')
    test_predicate = URIRef('http://www.w3.org/2000/01/rdf-schema#:label')
    test_object = 'String'

    await simple_insert(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj=test_object
    )
    results = await simple_select_object(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj='?string'
    )
    assert len(results) == 1
    assert results[0]['string'] == test_object


@pytest.mark.asyncio
async def test_int_literal(
    jena_client, truncate_jena, simple_insert, simple_select_object
):
    test_subject = URIRef('http://test.com')
    test_predicate = URIRef('http://www.w3.org/2000/01/rdf-schema#:label')
    test_object = 1

    await simple_insert(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj=test_object
    )

    results = await simple_select_object(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj='?integer'
    )
    assert len(results) == 1
    assert results[0]['integer'] == test_object


@pytest.mark.asyncio
async def test_int_literal_iter(
    jena_client, truncate_jena, simple_insert, simple_select_object
):
    test_subject = URIRef('http://test.com')
    test_predicate = URIRef('http://www.w3.org/2000/01/rdf-schema#:label')
    test_object = 1

    await simple_insert(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj=test_object
    )

    results = await jena_client.query(
        """
        SELECT ?integer
        WHERE {{
          GRAPH <urn:x-arq:DefaultGraph> {{
            {subj} {pred} ?integer .
            FILTER(?integer IN {test_objects})
          }}
        }}
        """, {
            'subj': test_subject,
            'pred': test_predicate,
            'test_objects': tuple([test_object, ])
        }
    )
    assert len(results) == 1
    assert results[0]['integer'] == test_object
