from quantum_protocols import alice_prepare_qubits, eve_interception, bob_measure_qubits
from crypto_utils import privacy_amplification, encrypt_message, decrypt_message

# Configuration
num_bits = 100
enable_eve = True  # Toggle this to False to see a successful exchange
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
    
#Features a Machine Learning diagnostic layer to distinguish between quantum decoherence and malicious interception.
from quantum_protocols import alice_prepare_qubits, eve_interception, bob_measure_qubits
from crypto_utils import privacy_amplification, encrypt_message, decrypt_message
from noise_sim import get_noise_model
from security_ai import train_security_model, analyze_security

# --- Setup ---
num_bits = 100
enable_eve = True
hardware_error_rate = 0.02 # 2% chance of hardware error
ai_model = train_security_model()

# 1. Quantum Phase (with Noise)
alice_bits, alice_bases, circuits = alice_prepare_qubits(num_bits)
if enable_eve:
    circuits = eve_interception(circuits, num_bits)

# Apply noise during Bob's measurement
noise = get_noise_model(hardware_error_rate)
bob_bases, bob_results = bob_measure_qubits(circuits, num_bits, noise_model=noise)

# 2. Sifting
alice_key = [alice_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
bob_key = [bob_results[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]

# 3. AI Security Analysis
errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
qber = (errors / len(alice_key)) * 100 if alice_key else 100

security_report = analyze_security(ai_model, qber, len(alice_key), num_bits)

print(f"--- Diagnostic Report ---")
print(f"Measured QBER: {qber:.2f}%")
print(f"AI Analysis: {security_report}")

# 4. Final Encryption Logic
if qber < 11.0: # Even with AI, we keep the strict safety threshold for encryption
    a_final = privacy_amplification(alice_key)
    b_final = privacy_amplification(bob_key)
    encrypted = encrypt_message("Secret Data", a_final)
    print(f"Decrypted Message: {decrypt_message(encrypted, b_final)}")
else:
    print("Communication blocked for safety.")






















