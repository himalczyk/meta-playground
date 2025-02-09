import hashlib
import json
from datetime import datetime
from typing import Optional

from db.keydb_client import KeyDBClient

from .dto import BlockDTO, TransactionDTO
from .merkle_tree import MerkleTree
from .models import BlockModel


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
        tx_parts = [tx.tx_hash, tx.from_address, tx.to_address, tx.value, tx.gas_price, str(tx.gas_used)]
        return ":".join(tx_parts)

    def hash_function(self, data: str) -> str:
        """Returns SHA-256 hash of input data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def calculate_hash(self) -> str:
        """Compute the block's hash."""
        block_parts = [
            str(self.timestamp),
            self.prev_hash,
            str(self.merkle_root),
            str(self.block_number),
            self.block_hash,
            str(self.gas_used),
            str(self.gas_limit),
        ]
        block_content = "".join(block_parts)
        return self.hash_function(block_content)

    def __repr__(self) -> str:
        return (
            f"Block(Hash: {self.block_hash}, Number: {self.block_number}, "
            f"Prev: {self.prev_hash}, Merkle Root: {self.merkle_root})"
        )


class PersistentBlockchainHandler:
    def __init__(self, keydb_client: Optional[KeyDBClient] = None) -> None:
        """Initialize KeyDB client."""
        self.db = keydb_client or KeyDBClient()
        self.chain: list[Block] = []

    async def initialize(self) -> None:
        """Initialize the blockchain by loading existing chain data."""
        await self.load_chain()

    async def __aenter__(self) -> "PersistentBlockchainHandler":
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()

    async def store_block(self, block: Block) -> None:
        """Stores a block in KeyDB and adds it to the in-memory chain."""
        block_model = BlockModel.model_validate(block)
        await self.db.set(block.block_hash, block_model.model_dump_json())
        self.chain.append(block)
        # Store only block hashes in KeyDB for chain reconstruction
        chain_hashes = [block.block_hash for block in self.chain]
        await self.db.set("blockchain_chain", json.dumps(chain_hashes))

    async def load_chain(self) -> None:
        """Loads the blockchain from KeyDB and reconstructs Block objects."""
        chain_data = await self.db.get("blockchain_chain")
        if chain_data:
            block_hashes = json.loads(chain_data)
            self.chain = []
            for block_hash in block_hashes:
                block_data = await self.get_block(block_hash)
                if block_data:
                    block_model = BlockModel.model_validate(block_data)
                    block_dto = BlockDTO(
                        timestamp=block_model.timestamp,
                        parent_hash=block_model.prev_hash,
                        transactions=block_model.transactions,
                        block_number=block_model.block_number,
                        block_hash=block_model.block_hash,
                        gas_used=block_model.gas_used,
                        gas_limit=block_model.gas_limit,
                    )
                    self.chain.append(Block(block_dto))

    async def get_block(self, block_hash: str) -> dict:
        """Retrieves a block from KeyDB by its hash."""
        block_data = await self.db.get(block_hash)
        return json.loads(block_data) if block_data else {}

    async def close(self) -> None:
        """Close the KeyDB connection pool."""
        await self.db.close()
