# My blockchain playground

[![Python Application CI](https://github.com/himalczyk/meta-playground/actions/workflows/python-app.yml/badge.svg)](https://github.com/himalczyk/meta-playground/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/himalczyk/meta-playground/branch/master/graph/badge.svg)](https://codecov.io/gh/himalczyk/meta-playground)

Just a playground for me to learn about blockchain technology.
Going full improvisation here. Learning about blockchain by building one and creating a version of it with my own understanding.

# What I want to create

Is a simple blockchain implementation in Python that consists of blocks and transactions. The blocks have correctly hashed transactions with Merkle Tree to verify the integrity of the transactions. I want to implement a blockchain that will be a linked list of blocks. The blocks in the blockchain will will be stored in KeyDB for simplicity and speed.For transactions I want to use ERC20 standard and implement a simple contract that will be used to send fake USD to other addresses. 

I want to also implement a simple proof of work algorithm to mine new blocks.
And I also want to implement a simple REST API to interact with the blockchain.


# Tech stack

# Technologies

- Python
- FastAPI
- Pydantic
- KeyDB
- Pytest
- aiohttp/asyncio

# Linters

- Black
- Flake8
- Mypy
- Bandit
- Coverage
- Isort


# Merkle Tree Implementation

## What is a Merkle Tree?
A Merkle Tree is a data structure used in cryptography and blockchain technology that allows efficient and secure verification of large datasets. It's particularly useful in blockchain systems to verify transactions without needing to store the entire blockchain.

## How Does It Work?
1. Each transaction is hashed using a cryptographic hash function (SHA-256)
2. These hashes are paired up and hashed again
3. This process continues recursively until you get a single hash - the Merkle Root
4. If there's an odd number of transactions, the last one is duplicated

## Merkle Proof
A Merkle Proof allows you to verify whether a specific transaction exists in a Merkle Tree without revealing the entire tree. Here's how it works:

1. Find the transaction's hash in the first layer
2. Store only the necessary sibling hashes (not the entire tree)
3. Use these sibling hashes to reconstruct the Merkle Root
4. If the computed root matches the real root, the transaction is verified

## Code Structure

### `MerkleTree` Class
The main class that handles the creation and verification of the Merkle Tree.

#### Methods:
- `__init__(transactions: list[str])`: Creates a new Merkle Tree from a list of transactions
- `hash_function(data: str)`: Converts input data into a SHA-256 hash
- `build_merkle_tree()`: Constructs the tree and returns the Merkle Root
- `get_merkle_root()`: Returns the root hash of the tree
- `get_merkle_proof(transaction: str)`: Generates proof that a transaction exists in the tree
- `verify_merkle_proof(transaction, proof, root)`: Verifies if a transaction is part of the tree

### `Block` Class
Represents a block in a blockchain, using the Merkle Tree for transaction verification.

#### Methods:
- `__init__(transactions: list[str], prev_hash: str)`: Creates a new block
- `hash_function(data: str)`: Creates a SHA-256 hash of the block data
- `calculate_hash()`: Computes the block's unique hash

## Example Usage

```python
# Create a Merkle Tree with transactions
transactions = ["Tx1", "Tx2", "Tx3", "Tx4"]
merkle_tree = MerkleTree(transactions)

# Get the Merkle Root
root = merkle_tree.get_merkle_root()

# Generate a proof for transaction "Tx3"
proof = merkle_tree.get_merkle_proof("Tx3")

# Verify the proof
is_valid = merkle_tree.verify_merkle_proof("Tx3", proof, root)
```


## Why Use Merkle Trees?

1. **Efficiency**: Instead of storing all transactions, you only need to store the Merkle Root
2. **Security**: Any change in transactions will result in a different Merkle Root
3. **Quick Verification**: You can verify if a transaction is included without downloading all transactions
4. **Space Saving**: Merkle Proofs are much smaller than the full transaction history

## Technical Details

### Hash Function
- Uses SHA-256 cryptographic hash function
- Converts any input string into a fixed-size 64-character hexadecimal string
- Example: "Hello" → "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"

### Tree Structure

```
Root Hash
/ \
Hash1 Hash2
/ \ / \
Hash3 Hash4 Hash5 Hash6
/ \ / \ / \ / \
Tx1 Tx2 Tx3 Tx4 Tx5 Tx6 Tx7 Tx8
```

### Merkle Proof Structure
- A list of hashes and their positions (left/right)
- Used to reconstruct the path from a transaction to the root
- Verification succeeds if the reconstructed root matches the true root

## Use Cases
- Blockchain transaction verification
- File integrity checking in distributed systems
- Peer-to-peer networks
- Git version control system
- Certificate transparency logs

## Requirements
- Python 3.9 or higher
- Built-in `hashlib` library for SHA-256 hashing


## Merkle Proof Example

Let's say we have a Merkle Tree with the following transactions:

```
Root Hash
/ \
Hash1 Hash2
/ \ / \
Hash3 Hash4 Hash5 Hash6
/ \ / \ / \ / \
Tx1 Tx2 Tx3 Tx4 Tx5 Tx6 Tx7 Tx8
```

To verify transaction "Tx3", we need to provide the following proof:

```
Proof:
- Sibling Hash: Hash3
- Direction: Left
- Sibling Hash: Hash4
- Direction: Right
- Sibling Hash: Hash5
- Direction: Left
- Sibling Hash: Hash6
- Direction: Right
```

## Merkle Proof Verification

To verify the proof, we need to reconstruct the path from the transaction to the root:

```
Reconstructed Root:
/ \
Hash1 Hash2
/ \ / \
Hash3 Hash4 Hash5 Hash6
```

Since the reconstructed root matches the original root, we can confirm that transaction "Tx3" is part of the Merkle Tree.

## Conclusion

Merkle Trees provide a secure and efficient way to verify the integrity of large datasets, making them invaluable in blockchain technology and distributed systems.
