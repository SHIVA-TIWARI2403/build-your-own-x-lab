import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1.0 - s)

class MiniNeuralNet:
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, learning_rate: float = 0.5, seed: int = 42):
        np.random.seed(seed)
        self.lr = learning_rate
        # Weights initialized with small random values
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.5
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.5
        self.b2 = np.zeros((1, output_dim))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output):
        m = X.shape[0]

        # Output layer error & delta
        # Loss = 0.5 * (output - y)^2 => dLoss/dOutput = (output - y)
        d_output = (output - y) * sigmoid_derivative(self.z2)
        dW2 = np.dot(self.a1.T, d_output) / m
        db2 = np.sum(d_output, axis=0, keepdims=True) / m

        # Hidden layer error & delta
        d_hidden = np.dot(d_output, self.W2.T) * sigmoid_derivative(self.z1)
        dW1 = np.dot(X.T, d_hidden) / m
        db1 = np.sum(d_hidden, axis=0, keepdims=True) / m

        # Gradient descent update
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def train(self, X, y, epochs: int = 5000):
        losses = []
        for epoch in range(epochs):
            output = self.forward(X)
            loss = np.mean((output - y) ** 2)
            losses.append(loss)
            self.backward(X, y, output)
        return losses

    def predict(self, X):
        probs = self.forward(X)
        return (probs > 0.5).astype(int)

if __name__ == "__main__":
    # Solving the classic non-linear XOR Problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    nn = MiniNeuralNet(input_dim=2, hidden_dim=4, output_dim=1, learning_rate=1.0)
    print("Training MiniNeuralNet on non-linear XOR...")
    losses = nn.train(X, y, epochs=4000)

    predictions = nn.predict(X)
    print(f"Final MSE Loss: {losses[-1]:.6f}")
    print("\nTruth vs Prediction:")
    for inp, target, pred in zip(X, y, predictions):
        print(f"Input: {inp} | Expected: {target[0]} | Predicted: {pred[0]}")
