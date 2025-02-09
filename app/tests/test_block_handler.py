from datetime import datetime
from typing import Self

import pytest
from blockchain.dto import BlockDTO, TransactionDTO
from blockchain.handler import Block, PersistentBlockchainHandler
from db.keydb_client import KeyDBClient


class MockKeyDBClient(KeyDBClient):
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str) -> None:
        self.store[key] = value

    async def close(self) -> None:
        pass


@pytest.fixture
def mock_keydb_client() -> MockKeyDBClient:
    return MockKeyDBClient()


@pytest.fixture
def sample_block_dto() -> BlockDTO:
    """Fixture providing sample test data."""
    transactions = [
        TransactionDTO(
            txHash="0x123",
            **{"from": "0xsender1"},
            **{"to": "0xreceiver1"},
            value="1.5",
            gasPrice="20",
            gasUsed=21000,
            blockNumber=1,
            timeStamp=datetime.now(),
        ),
        TransactionDTO(
            txHash="0x456",
            **{"from": "0xsender2"},
            **{"to": "0xreceiver2"},
            value="2.5",
            gasPrice="20",
            gasUsed=21000,
            blockNumber=1,
            timeStamp=datetime.now(),
        ),
    ]

    return BlockDTO(
        number=1,
        hash="0x789",  # Changed to match test expectation
        parentHash="0x000",
        timestamp=datetime.now(),
        transactions=transactions,  # Added sample transactions
        gasUsed=42000,
        gasLimit=15000000,
    )


@pytest.fixture(scope="function")
async def blockchain(mock_keydb_client: MockKeyDBClient) -> Self:
    chain = PersistentBlockchainHandler(mock_keydb_client)
    await chain.initialize()
    yield chain
    await chain.close()


@pytest.mark.asyncio
async def test_store_and_retrieve_block(mock_keydb_client: MockKeyDBClient, sample_block_dto: BlockDTO) -> None:
    """Test storing and retrieving a block."""
    async with PersistentBlockchainHandler(mock_keydb_client) as blockchain:
        block = Block(sample_block_dto)
        await blockchain.store_block(block)

        retrieved_block_data = await blockchain.get_block(block.block_hash)

        assert retrieved_block_data["block_number"] == block.block_number
        assert retrieved_block_data["block_hash"] == block.block_hash
        assert retrieved_block_data["prev_hash"] == block.prev_hash
        assert len(retrieved_block_data["transactions"]) == len(block.transactions)
        assert block.block_hash in [b.block_hash for b in blockchain.chain]


@pytest.mark.asyncio
async def test_load_chain(mock_keydb_client: MockKeyDBClient, sample_block_dto: BlockDTO) -> None:
    """Test loading chain from storage."""
    blocks = [Block(BlockDTO(**{**vars(sample_block_dto), "number": i + 1, "hash": f"0x{i+1}"})) for i in range(3)]

    async with PersistentBlockchainHandler(mock_keydb_client) as blockchain:
        # Store blocks
        for block in blocks:
            await blockchain.store_block(block)

        # Reload chain in same context
        await blockchain.load_chain()

        # Verify chain contents
        assert len(blockchain.chain) == len(blocks)
        for stored, original in zip(blockchain.chain, blocks):
            assert stored.block_hash == original.block_hash
            assert stored.block_number == original.block_number
            assert stored.prev_hash == original.prev_hash
            assert len(stored.transactions) == len(original.transactions)


class TestBlockHandler:
    def test_block_creation(self, sample_block_dto: BlockDTO) -> None:
        """Test creating a block and verifying its properties."""
        block = Block(sample_block_dto)

        assert block.block_number == 1
        assert block.block_hash == "0x789"
        assert block.prev_hash == "0x000"
        assert len(block.transactions) == 2  # Now we have 2 transactions
        assert block.merkle_root is not None  # Will pass because we have transactions
        assert block.gas_used == 42000
        assert block.gas_limit == 15000000

    def test_merkle_root_calculation(self, sample_block_dto: BlockDTO) -> None:
        """Test that merkle root is calculated correctly and is consistent."""
        block1 = Block(sample_block_dto)
        block2 = Block(sample_block_dto)

        assert block1.merkle_root is not None
        assert block2.merkle_root is not None
        assert block1.merkle_root == block2.merkle_root  # Same transactions should produce same root

    def test_transaction_verification(self, sample_block_dto: BlockDTO) -> None:
        """Test verifying a transaction using merkle proof."""
        block = Block(sample_block_dto)
        first_tx = sample_block_dto.transactions[0]

        # Convert transaction to string format used in merkle tree
        tx_string = block._transaction_to_string(first_tx)

        # Get and verify merkle proof
        proof = block.merkle_tree.get_merkle_proof(tx_string)
        assert proof is not None

        is_valid = block.merkle_tree.verify_merkle_proof(tx_string, proof, block.merkle_root)
        assert is_valid is True

    def test_hash_calculation(self, sample_block_dto: BlockDTO) -> None:
        """Test that block hash calculation is consistent."""
        block = Block(sample_block_dto)
        hash1 = block.calculate_hash()
        hash2 = block.calculate_hash()

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 character hex string
