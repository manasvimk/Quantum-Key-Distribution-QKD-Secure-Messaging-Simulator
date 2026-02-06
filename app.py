import streamlit as st
import numpy as np
from quantum_protocols import alice_prepare_qubits, bob_measure_qubits, eve_interception

st.title("🛡️ Quantum Security Dashboard")

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
num_bits = st.sidebar.slider("Number of Qubits", 10, 500, 100)
enable_eve = st.sidebar.checkbox("Enable Eavesdropper (Eve)")
noise_level = st.sidebar.slider("Hardware Noise Level", 0.0, 0.2, 0.02)

# --- Run Simulation ---
if st.button("Generate Quantum Key"):
    alice_bits, alice_bases, circuits = alice_prepare_qubits(num_bits)

    if enable_eve:
        st.warning("Eve is intercepting the channel...")
        circuits = eve_interception(circuits, num_bits)

    bob_bases, bob_results = bob_measure_qubits(circuits, num_bits)

    # Sifting Logic
    alice_key = [alice_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    bob_key = [bob_results[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]

    # Metrics
    errors = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
    qber = (errors / len(alice_key)) * 100 if alice_key else 100

    # --- Display Results ---
    col1, col2 = st.columns(2)
    col1.metric("Final Key Length", len(alice_key))
    col2.metric("QBER (Error Rate)", f"{qber:.2f}%")

    if qber > 11.0:
        st.error("🚨 SECURITY ALERT: High error rate detected. Connection Terminated.")
    else:
        st.success("✅ Secure Key Established.")