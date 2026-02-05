import numpy as np
from qiskit import QuantumCircuit


def alice_prepare_qubits(num_bits):
    # 1. Generate random bits (0 or 1)
    alice_bits = np.random.randint(2, size=num_bits)

    # 2. Generate random bases (0 for Standard '+', 1 for Diagonal 'x')
    alice_bases = np.random.randint(2, size=num_bits)

    circuits = []

    # 3. Create a circuit for each bit
    for i in range(num_bits):
        qc = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit

        # Encode the bit value
        if alice_bits[i] == 1:
            qc.x(0)  # Flip |0> to |1>

        # Apply the basis
        if alice_bases[i] == 1:
            qc.h(0)  # Rotate to Diagonal (x) basis

        circuits.append(qc)

    return alice_bits, alice_bases, circuits


# --- Let's test it ---
num_test_bits = 5
bits, bases, circuits = alice_prepare_qubits(num_test_bits)

print(f"Alice's Bits:  {bits}")
print(f"Alice's Bases: {bases} (0=Standard, 1=Diagonal)")

# Visualize the first qubit Alice prepared
print("\nCircuit for the first qubit:")
print(circuits[0].draw(output='text'))

#BOB's part starts here
from qiskit_aer import AerSimulator


def bob_measure_qubits(circuits, num_bits):
    # 1. Bob randomly chooses his bases (0 for +, 1 for x)
    bob_bases = np.random.randint(2, size=num_bits)
    bob_results = []

    simulator = AerSimulator()

    for i in range(num_bits):
        qc = circuits[i]

        # 2. If Bob chooses Diagonal (x), apply H-gate before measuring
        if bob_bases[i] == 1:
            qc.h(0)

        qc.measure_all()

        # 3. Run the simulation
        result = simulator.run(qc, shots=1, memory=True).result()
        # .split() removes spaces, and [0] takes the first bit in the list
        measured_bit = int(result.get_memory()[0].split()[0])
        bob_results.append(measured_bit)

    return bob_bases, np.array(bob_results)


# --- Test Bob's part with Alice's data ---
# (Assuming 'circuits' and 'num_test_bits' are from your previous Alice script)
bob_bases, bob_results = bob_measure_qubits(circuits, num_test_bits)

print(f"Bob's Bases:   {bob_bases}")
print(f"Bob's Results: {bob_results}")

# --- Sifting Step ---
final_alice_key = []
final_bob_key = []

for i in range(num_test_bits):
    if bits[i] == bob_bases[i]: # They compare bases
        final_alice_key.append(bits[i])
        final_bob_key.append(bob_results[i])

print(f"\nFinal Sifted Key (Alice): {final_alice_key}")
print(f"Final Sifted Key (Bob):   {final_bob_key}")

#EVE's part

def eve_interception(alice_circuits, num_bits):
    # 1. Eve randomly picks a basis to guess (0 for +, 1 for x)
    eve_bases = np.random.randint(2, size=num_bits)

    simulator = AerSimulator()

    for i in range(num_bits):
        qc = alice_circuits[i]

        # 2. Eve applies her guess basis
        if eve_bases[i] == 1:
          qc.h(0)

        # 3. Eve measures the qubit (This is what "ruins" it)
        qc.measure(0, 0)

        # 4. Eve must re-prepare the qubit in the basis she measured in
        # so Bob receives *something* that looks like a qubit
        result = simulator.run(qc, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0].split()[0])

        # Reset the qubit to the state Eve measured
        if measured_bit == 1:
            qc.x(0)
        if eve_bases[i] == 1:
            qc.h(0)

    return alice_circuits  # These are now the "disturbed" qubits

num_bits = 100

# 1. Alice prepares
alice_bits, alice_bases, circuits = alice_prepare_qubits(num_bits)

# 2. EVE INTERCEPTS!
circuits = eve_interception(circuits, num_bits)

# 3. Bob measures the disturbed qubits
bob_bases, bob_results = bob_measure_qubits(circuits, num_bits)

# 4. Sifting (Compare bases)
final_alice_key = []
final_bob_key = []

for i in range(num_bits):
    if alice_bases[i] == bob_bases[i]:
        final_alice_key.append(alice_bits[i])
        final_bob_key.append(bob_results[i])

# 5. Calculate Error Rate (QBER)
errors = 0
for a, b in zip(final_alice_key, final_bob_key):
    if a != b:
        errors += 1

error_rate = (errors / len(final_alice_key)) * 100

print(f"Key Length after sifting: {len(final_alice_key)}")
print(f"Number of errors found: {errors}")
print(f"Quantum Bit Error Rate (QBER): {error_rate:.2f}%")

import hashlib


def privacy_amplification(shared_key):
    # Convert the list of bits [1, 0, 1...] into a string "101..."
    key_string = "".join(map(str, shared_key))

    # Use SHA-256 to hash the string
    # This spreads the entropy and shrinks the key
    hashed_key = hashlib.sha256(key_string.encode()).hexdigest()

    return hashed_key


# Usage:
if error_rate < 11.0:  # Only proceed if the channel is relatively safe
    final_secure_key = privacy_amplification(final_alice_key)
    print(f"Final Secure Key (Hex): {final_secure_key}")
else:
    print("ALERT: Eavesdropper detected or noise too high. Protocol Aborted.")

    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import os


    def encrypt_message(message, hex_key):
        # 1. Convert hex key back to bytes
        key_bytes = bytes.fromhex(hex_key)

        # 2. Generate a random Initialization Vector (IV)
        # This ensures that even if you send the same message twice, the ciphertext looks different
        iv = os.urandom(16)

        # 3. Setup AES-CTR mode (no padding required, very fast)
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # 4. Encrypt the text
        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

        # We return the IV and the ciphertext together so Bob can decrypt it
        return iv + ciphertext


    def decrypt_message(encrypted_data, hex_key):
        key_bytes = bytes.fromhex(hex_key)

        # Extract the first 16 bytes (the IV) and the rest (the secret message)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and turn back into a string
        decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_message.decode()


    if error_rate < 11.0:
        # 1. Alice writes a message
        secret_note = "Meet me at the park at midnight."

        # 2. Alice encrypts it using her quantum-generated key
        encrypted_packet = encrypt_message(secret_note, final_alice_key)
        print(f"\nEncrypted Packet (What Eve sees): {encrypted_packet.hex()}")

        # 3. Bob decrypts it using his identical key
        decrypted_note = decrypt_message(encrypted_packet, final_bob_key)
        print(f"Bob's Decrypted Message: {decrypted_note}")