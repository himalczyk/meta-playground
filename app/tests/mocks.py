from typing import Self

import pytest


class MockKeyDBClient:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str) -> bool:
        self.store[key] = value
        return True

    async def close(self) -> None:
        self.store.clear()


@pytest.fixture(scope="function")
async def mock_keydb_client() -> Self:
    client = MockKeyDBClient()
    yield client
    await client.close()
