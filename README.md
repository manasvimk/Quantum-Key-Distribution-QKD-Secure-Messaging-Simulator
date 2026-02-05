# Quantum-Key-Distribution-QKD-Secure-Messaging-Simulator
A Python-based simulation of the BB84 Quantum Key Distribution protocol featuring an active eavesdropper module, QBER analysis, and AES-256 encrypted messaging

Overview

This project is a full-stack implementation of the BB84 Quantum Key Distribution protocol using IBM’s Qiskit. It simulates a quantum-to-classical pipeline where two parties (Alice and Bob) establish a secure cryptographic key through a simulated quantum channel, detect eavesdropping, and use the resulting key for AES-256 encrypted communication.

Key Features-

1)Quantum Bit Generation: Alice encodes classical bits into quantum states (qubits) using random bases (Standard and Diagonal).

2)Active Eavesdropper (Eve) Simulation: A 'Man-in-the-Middle' module that intercepts, measures, and resends qubits, demonstrating how quantum measurement disturbs information.

3)Security Monitoring (QBER): Calculates the Quantum Bit Error Rate to detect the presence of an intruder.

4)Privacy Amplification: Implements SHA-256 hashing to compress the sifted key, ensuring near-zero information leakage to the eavesdropper.

5)AES-256 Encrypted Chat: A practical application layer that uses the quantum-generated key to encrypt and decrypt text messages using AES-CTR mode.

The Protocol Logic:

Quantum Phase: Alice sends qubits and  Bob measures them.

Sifting Phase: Alice and Bob publicly share their bases and keep only the bits where their bases match.

Error Check: If the error rate (QBER) exceeds 11%, the protocol aborts due to suspected eavesdropping.

Amplification Phase: If the channel is secure, the bits are hashed into a final 256-bit key.

Application Phase: The key is used for symmetric encryption of a message.

Technologies Used:
1) Qiskit: Quantum circuit design and simulation.

2) Python: Core logic and sifting algorithms.

3) NumPy: High-performance data processing for bit arrays.

4) Cryptography (hazmat): Industry-standard AES-256 implementation.

Hashlib: SHA-256 for privacy amplification.
