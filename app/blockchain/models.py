# Reserved for future model implementations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from .dto import BlockDTO, TransactionDTO


class TransactionModel(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    value: str
    gas_price: str
    gas_used: int
    timeStamp: datetime

    class Config:
        from_attributes = True  # Allows conversion from ORM/DTO objects


class BlockModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    prev_hash: str
    merkle_root: str | None
    block_number: int
    block_hash: str
    gas_used: int
    gas_limit: int
    transactions: List[TransactionDTO]


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, block_dto: BlockDTO) -> None:
        self.timestamp: datetime = block_dto.timestamp
        self.prev_hash: str = block_dto.parent_hash
        self.block_number: int = block_dto.block_number
        self.block_hash: str = block_dto.block_hash
        self.gas_used: int = block_dto.gas_used
        self.gas_limit: int = block_dto.gas_limit
        self.transactions: list[TransactionDTO] = block_dto.transactions
        self.merkle_root: str | None = None

    def __repr__(self) -> str:
        return (
            f"Block(Hash: {self.block_hash}, Number: {self.block_number}, "
            f"Prev: {self.prev_hash}, Merkle Root: {self.merkle_root})"
        )
