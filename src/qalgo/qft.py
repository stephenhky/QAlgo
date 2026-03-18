
# quantum Fourier transform
# Qiskit convention: Little-Endian

import numpy as np
from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister


def QuantumFourierTransformGate(nbqubits: int) -> Gate:
    register = QuantumRegister(nbqubits)
    qc = QuantumCircuit(register)

    for i in range(nbqubits):
        qc.h(register[i])
        if i < nbqubits:
            for j in range(i+1):
                qc.cu(0.,0., np.pi/2**(i+1-j), 0.,register[i+1], register[j])

    return qc.to_gate()
