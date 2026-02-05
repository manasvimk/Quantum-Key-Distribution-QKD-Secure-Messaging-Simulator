import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def alice_prepare_qubits(num_bits):
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits)
    circuits = []

    for i in range(num_bits):
        qc = QuantumCircuit(1, 1)
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
        circuits.append(qc)
    return alice_bits, alice_bases, circuits


def eve_interception(alice_circuits, num_bits):
    eve_bases = np.random.randint(2, size=num_bits)
    simulator = AerSimulator()

    for i in range(num_bits):
        qc = alice_circuits[i]
        if eve_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)

        result = simulator.run(qc, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])

        qc.reset(0)  # Clear for Bob
        if measured_bit == 1:
            qc.x(0)
        if eve_bases[i] == 1:
            qc.h(0)
    return alice_circuits


def bob_measure_qubits(circuits, num_bits):
    bob_bases = np.random.randint(2, size=num_bits)
    bob_results = []
    simulator = AerSimulator()

    for i in range(num_bits):
        qc = circuits[i]
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)
        result = simulator.run(qc, shots=1, memory=True).result()
        bob_results.append(int(result.get_memory()[0]))
    return bob_bases, np.array(bob_results)