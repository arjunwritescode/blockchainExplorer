# from flask import Flask, render_template, jsonify
# import hashlib
# import time
# import json
# from Crypto.PublicKey import RSA
# from Crypto.Signature import pkcs1_15
# from Crypto.Hash import SHA256

# app = Flask(__name__)

# # Your existing cryptocurrency code

# REWARD = 50
# DIFFICULTY = 4

# class Transaction:
#     def __init__(self, sender, receiver, amount, signature=None):
#         self.sender = sender
#         self.receiver = receiver
#         self.amount = amount
#         self.signature = signature

#     def to_dict(self):
#         return {
#             "sender": self.sender,
#             "receiver": self.receiver,
#             "amount": self.amount,
#             "signature": self.signature
#         }

#     def __repr__(self):
#         return f"{self.sender} -> {self.receiver}: {self.amount}"

#     def sign_transaction(self, private_key):
#         h = SHA256.new(json.dumps(self.to_dict(), sort_keys=True).encode('utf-8'))
#         self.signature = pkcs1_15.new(private_key).sign(h)

#     def is_valid(self):
#         if self.sender == "MINING":
#             return True
#         if not self.signature or len(self.signature) == 0:
#             return False
#         h = SHA256.new(json.dumps(self.to_dict(), sort_keys=True).encode('utf-8'))
#         try:
#             public_key = RSA.import_key(self.sender)
#             pkcs1_15.new(public_key).verify(h, self.signature)
#             return True
#         except (ValueError, TypeError):
#             return False

# class Block:
#     def __init__(self, index, previous_hash, timestamp, transactions, proof_of_work, hash):
#         self.index = index
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.transactions = transactions
#         self.proof_of_work = proof_of_work
#         self.hash = hash

# def calculate_hash(block):
#     block_string = json.dumps({
#         "index": block.index,
#         "previous_hash": block.previous_hash,
#         "timestamp": block.timestamp,
#         "transactions": [t.to_dict() for t in block.transactions],
#         "proof_of_work": block.proof_of_work
#     }, sort_keys=True).encode('utf-8')

#     return hashlib.sha256(block_string).hexdigest()

# def proof_of_work(last_proof, difficulty):
#     proof = 0
#     while not is_valid_proof(last_proof, proof, difficulty):
#         proof += 1
#     return proof

# def is_valid_proof(last_proof, proof, difficulty):
#     guess = f'{last_proof}{proof}'.encode('utf-8')
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     return guess_hash[:difficulty] == '0' * difficulty

# # Initialize blockchain
# blockchain = []
# blockchain.append(create_genesis_block())

# # Add block with transactions
# new_block = add_block(blockchain[-1])
# blockchain.append(new_block)

# # Your Flask routes

# @app.route('/')
# def index():
#     return render_template('index.html', blockchain=blockchain)

# @app.route('/api/blocks')
# def get_blocks():
#     blocks_json = [{
#         "index": block.index,
#         "previous_hash": block.previous_hash,
#         "timestamp": block.timestamp,
#         "transactions": [t.to_dict() for t in block.transactions],
#         "proof_of_work": block.proof_of_work,
#         "hash": block.hash
#     } for block in blockchain]

#     return jsonify(blocks_json)

# if __name__ == '__main__':
#     app.run(debug=True)
import matplotlib.pyplot as plt
# Bitcoin Replica

import hashlib
import time
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

REWARD = 50  # Set reward for mining a block

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def __repr__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

    def sign_transaction(self, private_key):
        h = SHA256.new(str(self).encode('utf-8'))
        self.signature = pkcs1_15.new(private_key).sign(h)

    def is_valid(self):
        if self.sender == "MINING":
            return True
        if not self.signature or len(self.signature) == 0:
            return False
        h = SHA256.new(str(self).encode('utf-8'))
        try:
            public_key = RSA.import_key(self.sender)
            pkcs1_15.new(public_key).verify(h, self.signature)
            return True
        except (ValueError, TypeError):
            return False

# Mempool to hold transactions
mempool = []

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof_of_work, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.hash = calculate_hash(self)

def calculate_hash(block):
    return hashlib.sha256(f'{block.index}{block.previous_hash}{block.timestamp}{block.transactions}{block.proof_of_work}'.encode('utf-8')).hexdigest()

def proof_of_work(last_proof):
    proof = last_proof + 1
    while not (proof + last_proof) % 7 == 0:  # Simplified PoW, not secure.
        proof += 1
    return proof

# Generate keys for sender and receiver
miner_key = RSA.generate(2048)
receiver_key = RSA.generate(2048)

# Create transactions and add them to the mempool
transaction1 = Transaction(miner_key.publickey().exportKey(), receiver_key.publickey().exportKey(), 10)
transaction1.sign_transaction(miner_key)
mempool.append(transaction1)

# ... More code for peer-to-peer, validation, rewards, and smart contracts ...

# Add a block with transactions from mempool
def add_block(prev_block):
    index = prev_block.index + 1
    timestamp = time.time()
    proof = proof_of_work(prev_block.proof_of_work)
    current_transactions = mempool[:10]  # Take 10 transactions from mempool
    del mempool[:10]  # Remove them from mempool

    # Reward the miner (here, assume miner is the one calling this function)
    mining_reward = Transaction("MINING", miner_key.publickey().exportKey(), REWARD)
    current_transactions.append(mining_reward)

    hash = calculate_hash(prev_block)
    return Block(index, prev_block.hash, timestamp, current_transactions, proof, hash)

# Initialize blockchain
genesis_block = Block(0, '0', time.time(), [], 0, calculate_hash(Block(0, '0', time.time(), [], 0, '0')))
blockchain = [genesis_block]

# Add block with transactions
new_block = add_block(genesis_block)
blockchain.append(new_block)

# Print blockchain
for block in blockchain:
    print(f"Index: {block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Transactions: {block.transactions}")
    print(f"Hash: {block.hash}\n")



# Function to visualize the blockchain
def visualize_blockchain(blockchain):
    for block in blockchain:
        # Plot block index and hash
        plt.scatter(block.index, int(block.hash, 16), color='blue', s=100, label='Block')

        # Plot transactions within the block
        for i, transaction in enumerate(block.transactions):
            plt.scatter(block.index, int(transaction.hash, 16), color='red', s=50, label=f'Transaction {i + 1}')

    # Customize plot
    plt.title('Blockchain Visualization')
    plt.xlabel('Block Index')
    plt.ylabel('Hash (numeric representation)')
    plt.legend()
    plt.show()

# Initialize blockchain
genesis_block = Block(0, '0', time.time(), [], 0, calculate_hash(Block(0, '0', time.time(), [], 0, '0')))
blockchain = [genesis_block]

# Add block with transactions
new_block = add_block(blockchain[-1])
blockchain.append(new_block)

# Visualize the blockchain
visualize_blockchain(blockchain)
