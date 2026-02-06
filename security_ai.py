from sklearn.tree import DecisionTreeClassifier
import numpy as np


def train_security_model():
    # Training Data: [QBER, Key_Length_Ratio]
    # Label 0: Just Hardware Noise (Low Error)
    # Label 1: Eve Interception (High Error)

    X = np.array([
        [2.0, 0.5], [3.5, 0.48], [1.5, 0.52],  # Typical Noise (Label 0)
        [25.4, 0.5], [30.1, 0.49], [48.5, 0.51]  # Eve's interception (Label 1)
    ])
    y = np.array([0, 0, 0, 1, 1, 1])

    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model


def analyze_security(model, qber, key_length, initial_length):
    ratio = key_length / initial_length
    prediction = model.predict([[qber, ratio]])

    if prediction[0] == 1:
        return "CRITICAL: Pattern matches Active Interception (Eve)."
    else:
        return "NORMAL: Pattern matches Hardware Noise."