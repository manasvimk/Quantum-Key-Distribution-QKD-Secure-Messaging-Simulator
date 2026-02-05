from quantum_protocols import alice_prepare_qubits, eve_interception, bob_measure_qubits
from crypto_utils import privacy_amplification, encrypt_message, decrypt_message

# Configuration
num_bits = 100
enable_eve = True  # Toggle this to False to see a successful exchange!

# 1. Quantum Phase
alice_bits, alice_bases, circuits = alice_prepare_qubits(num_bits)
if enable_eve:
    circuits = eve_interception(circuits, num_bits)
bob_bases, bob_results = bob_measure_qubits(circuits, num_bits)

# 2. Sifting Phase
alice_key = [alice_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
bob_key = [bob_results[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]

# 3. Error Analysis
errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
qber = (errors / len(alice_key)) * 100 if alice_key else 100
print(f"Sifted Key Length: {len(alice_key)} | QBER: {qber:.2f}%")

# 4. Security Threshold Check
if qber < 11.0:
    a_final = privacy_amplification(alice_key)
    b_final = privacy_amplification(bob_key)
    msg = "Quantum communication is the future!"
    encrypted = encrypt_message(msg, a_final)
    print(f"Decrypted: {decrypt_message(encrypted, b_final)}")
else:
    print("ALERT: Eavesdropper detected. Aborting mission.")