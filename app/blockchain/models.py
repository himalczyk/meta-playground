# Reserved for future model implementations

from datetime import datetime

from .dto import BlockDTO, TransactionDTO
from .merkle_tree import MerkleTree


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
        return f"Block(Hash: {self.block_hash}, Number: {self.block_number}, Prev: {self.prev_hash}, Merkle Root: {self.merkle_root})"
