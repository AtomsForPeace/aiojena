#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name: conftest.py

import pytest
from aiojena.client import JenaClient


@pytest.fixture
async def jena_client():
    async with JenaClient('http://localhost:3030/') as jc:
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
