# 🧠 05 - Mini-Neural-Net

A multi-layer feedforward artificial neural network implemented in pure Python and NumPy from first mathematical principles, with zero reliance on PyTorch, TensorFlow, or Scikit-Learn.

---

## 🚀 Key Features

* **Dense Layer Architecture:** Configurable input, hidden, and output dimensionality with weight matrices and bias vectors.
* **Activation Functions:** Sigmoid activation $\sigma(z) = \frac{1}{1 + e^{-z}}$ and its analytical derivative $\sigma'(z) = \sigma(z)(1 - \sigma(z))$.
* **Forward Propagation:** Layer-by-layer linear combination and non-linear activation.
* **Backpropagation & Gradient Descent:** Full chain-rule gradient calculation ($\frac{\partial L}{\partial W}$, $\frac{\partial L}{\partial b}$) to iteratively minimize Mean Squared Error (MSE).
* **Solves Non-Linear Problems:** Accurately learns the XOR non-linear decision boundary with 100% precision.

---

## 🏃 Quick Usage

```bash
python neural_net.py
```

---

## 🧪 Testing

```bash
python test_neural_net.py
```
