import hashlib
from datetime import datetime

from .dto import BlockDTO, TransactionDTO
from .merkle_tree import MerkleTree


class Block:
    def __init__(self, block_dto: BlockDTO) -> None:
        """Initialize a new block from BlockDTO."""
        self.timestamp: datetime = block_dto.timestamp
        self.prev_hash: str = block_dto.parent_hash
        # Convert TransactionDTO objects to their string representations for Merkle Tree
        tx_strings = [self._transaction_to_string(tx) for tx in block_dto.transactions]
        self.merkle_tree: MerkleTree = MerkleTree(tx_strings)
        self.merkle_root: str | None = self.merkle_tree.get_merkle_root()
        self.block_number: int = block_dto.block_number
        self.block_hash: str = block_dto.block_hash
        self.gas_used: int = block_dto.gas_used
        self.gas_limit: int = block_dto.gas_limit
        self.transactions: list[TransactionDTO] = block_dto.transactions

    def _transaction_to_string(self, tx: TransactionDTO) -> str:
        """Convert a TransactionDTO to a consistent string representation."""
        return f"{tx.tx_hash}:{tx.from_address}:{tx.to_address}:{tx.value}:{tx.gas_price}:{tx.gas_used}"

    def hash_function(self, data: str) -> str:
        """Returns SHA-256 hash of input data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def calculate_hash(self) -> str:
        """Compute the block's hash."""
        block_content: str = (
            f"{self.timestamp}{self.prev_hash}{self.merkle_root}{self.block_number}{self.block_hash}{self.gas_used}{self.gas_limit}"
        )
        return self.hash_function(block_content)

    def __repr__(self) -> str:
        return f"Block(Hash: {self.block_hash}, Number: {self.block_number}, Prev: {self.prev_hash}, Merkle Root: {self.merkle_root})"
