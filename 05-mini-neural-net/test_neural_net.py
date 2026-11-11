import unittest
import numpy as np
from neural_net import MiniNeuralNet

class TestMiniNeuralNet(unittest.TestCase):
    def test_xor_learning(self):
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([[0], [1], [1], [0]])

        nn = MiniNeuralNet(input_dim=2, hidden_dim=4, output_dim=1, learning_rate=1.0, seed=42)
        initial_loss = np.mean((nn.forward(X) - y) ** 2)

        losses = nn.train(X, y, epochs=5000)
        final_loss = losses[-1]

        # Ensure loss decreased substantially
        self.assertLess(final_loss, initial_loss)
        self.assertLess(final_loss, 0.05)

        # Ensure 100% predictions on XOR truth table
        preds = nn.predict(X)
        np.testing.assert_array_equal(preds, y)

    def test_forward_shape(self):
        nn = MiniNeuralNet(input_dim=3, hidden_dim=5, output_dim=2)
        dummy_input = np.random.randn(10, 3)
        out = nn.forward(dummy_input)
        self.assertEqual(out.shape, (10, 2))

if __name__ == "__main__":
    unittest.main()
