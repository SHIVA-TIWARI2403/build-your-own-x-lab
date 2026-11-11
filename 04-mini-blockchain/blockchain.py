import hashlib
import json
import time

class Block:
    def __init__(self, index: int, timestamp: float, transactions: list, previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class MiniBlockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 50.0

    def create_genesis_block(self) -> Block:
        genesis = Block(0, 1700000000.0, ["Genesis Block - Systems from Scratch Lab"], "0" * 64, nonce=0)
        genesis.mine_block(self.difficulty)
        return genesis

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        if not sender or not recipient or amount <= 0:
            raise ValueError("Invalid transaction parameters")
        tx = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        }
        self.pending_transactions.append(tx)

    def mine_pending_transactions(self, miner_address: str) -> Block:
        # Create block with pending txs
        reward_tx = {
            "sender": "NETWORK_MINT",
            "recipient": miner_address,
            "amount": self.mining_reward,
            "timestamp": time.time()
        }
        txs_to_mine = self.pending_transactions + [reward_tx]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=txs_to_mine,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self) -> bool:
        target = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify current hash matches its contents
            if current.hash != current.calculate_hash():
                return False

            # Verify chain linkage
            if current.previous_hash != previous.hash:
                return False

            # Verify proof of work
            if not current.hash.startswith(target):
                return False

        return True

if __name__ == "__main__":
    bc = MiniBlockchain(difficulty=3)
    print("Genesis Block Hash:", bc.chain[0].hash)

    bc.add_transaction("Alice", "Bob", 15.5)
    bc.add_transaction("Bob", "Charlie", 5.0)

    print("\nMining block 1...")
    b1 = bc.mine_pending_transactions(miner_address="Shiva")
    print(f"Block 1 mined: {b1.hash} (Nonce: {b1.nonce})")

    print("\nIs chain valid?", bc.is_chain_valid())
