
from qiskit.circuit import QuantumRegister, QuantumCircuit, Gate


def GHZState(nbqubits: int) -> Gate:
    qr = QuantumRegister(nbqubits)
    qc = QuantumCircuit(qr)
    qc.h(qr[0])
    for i in range(1, nbqubits-1):
        qc.cx(qr[0], qr[i+1])
    return qc.to_gate()
