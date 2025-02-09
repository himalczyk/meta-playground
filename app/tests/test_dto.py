from datetime import datetime

import pytest
from blockchain.dto import BlockDTO, TransactionDTO
from pydantic import ValidationError


class TestTransactionDTO:
    def test_valid_transaction_creation(self) -> None:
        """Test creating a valid TransactionDTO."""
        tx = TransactionDTO(
            txHash="0x123",
            **{"from": "0xsender1"},
            **{"to": "0xreceiver1"},
            value="1.5",
            gasPrice="20",
            gasUsed=21000,
            blockNumber=1,
            timeStamp=datetime.now(),
        )

        assert tx.tx_hash == "0x123"
        assert tx.from_address == "0xsender1"
        assert tx.to_address == "0xreceiver1"
        assert tx.value == "1.5"
        assert tx.gas_price == "20"
        assert tx.gas_used == 21000
        assert tx.block_number == 1

    def test_invalid_transaction_missing_fields(self) -> None:
        """Test that TransactionDTO raises error when required fields are missing."""
        with pytest.raises(ValidationError):
            TransactionDTO(
                txHash="0x123",
                value="1.5",  # Missing from/to addresses
            )


class TestBlockDTO:
    def test_valid_block_creation(self) -> None:
        """Test creating a valid BlockDTO."""
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
            )
        ]

        block = BlockDTO(
            number=1,
            hash="0x789",
            parentHash="0x000",
            timestamp=datetime.now(),
            transactions=transactions,
            gasUsed=21000,
            gasLimit=15000000,
        )

        assert block.block_number == 1
        assert block.block_hash == "0x789"
        assert block.parent_hash == "0x000"
        assert len(block.transactions) == 1
        assert block.gas_used == 21000
        assert block.gas_limit == 15000000

    def test_block_with_no_transactions(self) -> None:
        """Test creating a block with empty transaction list."""
        block = BlockDTO(
            number=1,
            hash="0x789",
            parentHash="0x000",
            timestamp=datetime.now(),
            transactions=[],
            gasUsed=0,
            gasLimit=15000000,
        )

        assert len(block.transactions) == 0

    def test_invalid_block_missing_fields(self) -> None:
        """Test that BlockDTO raises error when required fields are missing."""
        with pytest.raises(ValidationError):
            BlockDTO(
                number=1,
                hash="0x789",
                # Missing parentHash
                timestamp=datetime.now(),
            )
