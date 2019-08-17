#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: test_uri.py

import pytest
from rdflib import URIRef


@pytest.mark.asyncio
async def test_uri(
    jena_client, truncate_jena, simple_insert, simple_select_predicate
):
    test_subject = URIRef('http://test.com')
    test_predicate = URIRef('http://www.w3.org/2000/01/rdf-schema#:label')
    test_object = 'Label'
    await simple_insert(
        jena_client=jena_client,
        subj=test_subject,
        pred=test_predicate,
        obj=test_object,
    )
    results = await simple_select_predicate(
        jena_client=jena_client,
        subj=test_subject,
        pred='?uri',
        obj=test_object,
    )
    assert len(results) == 1
    assert results[0]['uri'] == test_predicate.n3()
