from datetime import datetime

import pytest
from blockchain.dto import BlockDTO, TransactionDTO


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
