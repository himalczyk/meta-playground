import hashlib


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
            # bez reszty ffs
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
