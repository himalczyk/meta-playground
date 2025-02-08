import hashlib
import time

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


class MerkleTree:
    """
    Merkle Tree is a binary tree of hashes
    each transaction is hashed using SHA-256
    pairs of transactions hashes are combined and hashed again recursively
    if there is an odd number of transactions, the last one is duplicated
    the final hash is the -> Merkle Root
    """

    def __init__(self, transactions: list[str]) -> None:
        self._transactions: list[str] = transactions
        self._tree: list[list[str]] = []  # store all layers of the Merkle Tree
        self._root: str | None = self.build_merkle_tree()

    def hash_function(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def build_merkle_tree(self) -> str | None:
        """Builds the Merkle Tree and returns the Merkle Root."""
        if not self._transactions:
            return None  # No transactions

        # Step 1: Hash all transactions
        layer: list[str] = [self.hash_function(tx) for tx in self._transactions]
        self._tree = [layer]  # Initialize tree with leaf nodes

        # Step 2: Build the tree, storing each layer
        while len(layer) > 1:
            # If odd number of transactions, duplicate the last one
            if len(layer) % 2 == 1:
                layer.append(layer[-1])

            # Hash pairs together
            new_layer: list[str] = []
            for i in range(0, len(layer), 2):
                combined_hash = self.hash_function(layer[i] + layer[i + 1])
                new_layer.append(combined_hash)

            self._tree.append(new_layer)  # Store the new layer
            layer = new_layer

        return layer[0]  # The final root hash

    def get_merkle_root(self) -> str | None:
        """Returns the Merkle Root of the tree."""
        return self._root

    def get_tree(self) -> list[list[str]]:
        """Returns the entire tree."""
        return self._tree

    def get_merkle_proof(self, transaction: str) -> list[tuple[str, str]] | None:
        """
        Generates a Merkle Proof for a given transaction.
        Returns a list of (sibling hash, direction) tuples.
        """
        if transaction not in self._transactions:
            return None

        # Get the leaf node hash
        current_hash = self.hash_function(transaction)
        proof: list[tuple[str, str]] = []

        # Find position of transaction in leaf layer
        current_idx = self._tree[0].index(current_hash)

        # Go through each layer except the root
        for layer in self._tree[:-1]:
            # Is it a left node or right node?
            is_left = current_idx % 2 == 0

            if is_left:
                # If left node, get right sibling if it exists
                if current_idx + 1 < len(layer):
                    proof.append((layer[current_idx + 1], "right"))
            else:
                # If right node, get left sibling
                proof.append((layer[current_idx - 1], "left"))

            # Move to parent index in next layer
            current_idx //= 2

        return proof

    def verify_merkle_proof(self, transaction: str, proof: list[tuple[str, str]], root: str) -> bool:
        """
        Verifies a Merkle Proof by reconstructing the path to the root.
        """
        current_hash = self.hash_function(transaction)

        print("\nVerifying Merkle Proof for:", transaction)
        print("Starting Hash:", current_hash)

        for sibling_hash, direction in proof:
            print(f" → Combining {direction.upper()} sibling: {sibling_hash}")

            if direction == "left":
                current_hash = self.hash_function(sibling_hash + current_hash)
            else:  # direction == "right"
                current_hash = self.hash_function(current_hash + sibling_hash)

            print("   ↳ New Hash:", current_hash)

        print("Computed Root:", current_hash)
        print("Expected Root:", root)

        return current_hash == root


class Block:
    def __init__(self, transactions: list[str], prev_hash: str) -> None:
        """Initialize a new block."""
        self.timestamp: float = time.time()  # Block creation time
        self.prev_hash: str = prev_hash  # Link to previous block
        self.merkle_tree: MerkleTree = MerkleTree(transactions)  # Store transactions in Merkle Tree
        self.merkle_root: str | None = self.merkle_tree.get_merkle_root()
        self.nonce: int = 0  # Used for Proof of Work (if needed)
        self.hash: str = self.calculate_hash()  # Current block's hash

    def hash_function(self, data: str) -> str:
        """Returns SHA-256 hash of input data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def calculate_hash(self) -> str:
        """Compute the block's hash."""
        block_content: str = f"{self.timestamp}{self.prev_hash}{self.merkle_root}{self.nonce}"
        return self.hash_function(block_content)

    def __repr__(self) -> str:
        return f"Block(Hash: {self.hash}, Prev: {self.prev_hash}, Merkle Root: {self.merkle_root})"


if __name__ == "__main__":
    transactions: list[str] = ["Tx1", "Tx2", "Tx3", "Tx4"]

    # Create a new block (using a dummy previous hash)
    block: Block = Block(transactions, prev_hash="0000000000000000000000000000000000000000000000000000000000000000")

    print(f"Block Created: {block}")
    print(f"\nMerkle Root: {block.merkle_root}")

    # Generate a Merkle Proof for "Tx3" using the block's Merkle Tree
    proof = block.merkle_tree.get_merkle_proof("Tx3")
    print("\nMerkle Proof for Tx3:", proof)

    # Verify the Merkle Proof
    is_valid = block.merkle_tree.verify_merkle_proof("Tx3", proof, block.merkle_root)
    print("\nIs Tx3 Valid in the Block?", is_valid)
