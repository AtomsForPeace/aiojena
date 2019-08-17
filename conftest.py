#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: conftest.py

from typing import List
import pytest
from aiojena.client import JenaClient


@pytest.fixture
async def jena_client():
    async with JenaClient('http://localhost:3030/test') as jc:
        yield jc


@pytest.fixture
async def truncate_jena(jena_client: JenaClient):
    await jena_client.update(
        """
        DELETE
        WHERE {
          ?s ?p ?o
        }
        """
    )


@pytest.fixture
async def simple_insert():
    async def _simple_insert(jena_client, subj, pred, obj) -> None:
        await jena_client.update(
            """
            INSERT DATA {{
            {subj}     {pred}      {obj}
            }}
            """, {
                'subj': subj,
                'pred': pred,
                'obj': obj
            }
        )
    return _simple_insert


@pytest.fixture
async def simple_select_predicate():
    async def _simple_select_predicate(jena_client, subj, pred, obj) -> List:
        return await jena_client.query(
            """
            SELECT {pred}
            WHERE {{
            {subj}     {pred}      {obj}
            }}
            """, {
                'subj': subj,
                'pred': pred,
                'obj': obj
            }
        )
    return _simple_select_predicate


@pytest.fixture
async def simple_select_object():
    async def _simple_select_object(jena_client, subj, pred, obj) -> List:
        return await jena_client.query(
            """
            SELECT {obj}
            WHERE {{
            {subj}     {pred}      {obj}
            }}
            """, {
                'subj': subj,
                'pred': pred,
                'obj': obj
            }
        )
    return _simple_select_object
