from qiskit_aer.noise import NoiseModel, depolarizing_error

def get_noise_model(prob):
    """
    Creates a noise model where qubits have a 'prob' chance of
    flipping/changing state during a gate operation.
    """
    noise_model = NoiseModel()

    error = depolarizing_error(prob, 1)
    noise_model.add_all_qubit_quantum_error(error, ['h', 'x', 'id'])
    return noise_model