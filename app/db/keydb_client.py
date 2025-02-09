from typing import Any

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from redis.asyncio.retry import Retry


class KeyDBClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        max_connections: int = 10,
        decode_responses: bool = True,
    ) -> None:
        retry = Retry(max_attempts=3, backoff=1)
        self.pool = ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=decode_responses,
            retry=retry,
        )
        self.client: redis.Redis = redis.Redis(connection_pool=self.pool)

    async def get(self, key: str) -> Any:
        """Get value for key."""
        return await self.client.get(key)

    async def set(self, key: str, value: str) -> bool:
        """Set key to value."""
        return await self.client.set(key, value)

    async def delete(self, key: str) -> bool:
        """Delete key."""
        return bool(await self.client.delete(key))

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return bool(await self.client.exists(key))

    async def close(self) -> None:
        """Close all connections in the pool."""
        await self.pool.disconnect()
