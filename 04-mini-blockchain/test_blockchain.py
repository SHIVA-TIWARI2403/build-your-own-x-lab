import unittest
from blockchain import MiniBlockchain

class TestMiniBlockchain(unittest.TestCase):
    def setUp(self):
        self.bc = MiniBlockchain(difficulty=2)

    def test_genesis_block(self):
        self.assertEqual(len(self.bc.chain), 1)
        self.assertEqual(self.bc.chain[0].index, 0)
        self.assertTrue(self.bc.chain[0].hash.startswith("00"))

    def test_mining_and_chain_validity(self):
        self.bc.add_transaction("Alice", "Bob", 10.0)
        self.bc.add_transaction("Bob", "Charlie", 2.5)
        b1 = self.bc.mine_pending_transactions(miner_address="Miner1")

        self.assertEqual(len(self.bc.chain), 2)
        self.assertEqual(b1.previous_hash, self.bc.chain[0].hash)
        self.assertTrue(b1.hash.startswith("00"))
        self.assertTrue(self.bc.is_chain_valid())

    def test_tamper_detection(self):
        self.bc.add_transaction("Alice", "Bob", 50.0)
        self.bc.mine_pending_transactions(miner_address="Miner1")
        self.assertTrue(self.bc.is_chain_valid())

        # Attempt to tamper with transaction amount in block 1
        self.bc.chain[1].transactions[0]["amount"] = 99999.0

        # Chain must immediately become invalid
        self.assertFalse(self.bc.is_chain_valid())

if __name__ == "__main__":
    unittest.main()
