from datetime import datetime

from blockchain.dto import BlockDTO, TransactionDTO
from blockchain.handler import Block

# hash each transaction into crypto hash
# pair up hashes and hash again - recursively combine until you get a merkle root
# if odd number of transactions, duplicate last one
# return the merkle root

# How a Merkle Proof Works
# Merkle Tree implementation to support Merkle Proofs.
# A Merkle Proof allows you to verify whether a specific transaction
# exists in a Merkle Tree without revealing the entire tree.
# If you want to prove that a transaction (e.g., Tx3) is in a block:

# Find the transaction's hash in the first layer.
# Store only the necessary sibling hashes (not the entire tree).
# Use these sibling hashes to reconstruct the Merkle Root.
# If the computed root matches the real root, the transaction is verified.


if __name__ == "__main__":
    transactions: list[TransactionDTO] = [
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

    block_dto: BlockDTO = BlockDTO(
        number=1,
        hash="0x789",
        parentHash="0x000",
        timestamp=datetime.now(),
        transactions=transactions,
        gasUsed=42000,
        gasLimit=15000000,
    )

    block = Block(block_dto)

    print(f"Block Created: {block}")
    print(f"\nMerkle Root: {block.merkle_root}")

    # Generate a Merkle Proof for the first transaction
    first_tx_string = block._transaction_to_string(transactions[0])
    proof = block.merkle_tree.get_merkle_proof(first_tx_string)
    print("\nMerkle Proof for first transaction:", proof)

    # Verify the Merkle Proof
    is_valid = block.merkle_tree.verify_merkle_proof(first_tx_string, proof, block.merkle_root)
    print("\nIs First Transaction Valid in the Block?", is_valid)
