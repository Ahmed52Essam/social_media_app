import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

os.environ["ENV_STATE"] = "test"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    from social_media_app.main import app

    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    from social_media_app.database import database

    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    from social_media_app.main import app

    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
