from datetime import datetime

import pytest
from blockchain.dto import BlockDTO, TransactionDTO
from blockchain.handler import BlockHandler


@pytest.fixture
def sample_transactions() -> list[TransactionDTO]:
    """Fixture providing sample transactions for testing."""
    return [
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


@pytest.fixture
def sample_block_dto(sample_transactions: list[TransactionDTO]) -> BlockDTO:
    """Fixture providing a sample BlockDTO for testing."""
    return BlockDTO(
        number=1,
        hash="0x789",
        parentHash="0x000",
        timestamp=datetime.now(),
        transactions=sample_transactions,
        gasUsed=42000,
        gasLimit=15000000,
    )


class TestBlockHandler:
    def test_block_creation(self, sample_block_dto: BlockDTO) -> None:
        """Test creating a block and verifying its properties."""
        block = BlockHandler(sample_block_dto)

        assert block.block_number == 1
        assert block.block_hash == "0x789"
        assert block.prev_hash == "0x000"
        assert len(block.transactions) == 2
        assert block.merkle_root is not None
        assert block.gas_used == 42000
        assert block.gas_limit == 15000000

    def test_merkle_root_calculation(self, sample_block_dto: BlockDTO) -> None:
        """Test that merkle root is calculated correctly and is consistent."""
        block1 = BlockHandler(sample_block_dto)
        block2 = BlockHandler(sample_block_dto)

        assert block1.merkle_root is not None
        assert block1.merkle_root == block2.merkle_root

    def test_transaction_verification(self, sample_block_dto: BlockDTO) -> None:
        """Test verifying a transaction using merkle proof."""
        block = BlockHandler(sample_block_dto)
        first_tx = sample_block_dto.transactions[0]

        # Get merkle proof for first transaction
        tx_string = block._transaction_to_string(first_tx)
        proof = block.merkle_tree.get_merkle_proof(tx_string)

        # Verify the proof
        is_valid = block.merkle_tree.verify_merkle_proof(tx_string, proof, block.merkle_root)
        assert is_valid is True

    def test_hash_calculation(self, sample_block_dto: BlockDTO) -> None:
        """Test that block hash calculation is consistent."""
        block = BlockHandler(sample_block_dto)
        hash1 = block.calculate_hash()
        hash2 = block.calculate_hash()

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 character hex string
