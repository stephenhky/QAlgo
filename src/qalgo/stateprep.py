
from qiskit.circuit import QuantumRegister, QuantumCircuit, Gate


def GHZState(nbqubits: int) -> Gate:
    qr = QuantumRegister(nbqubits)
    qc = QuantumCircuit(qr)
    qc.h(qr[0])
    for i in range(0, nbqubits-1):
        qc.cx(qr[0], qr[i+1])
    return qc.to_gate()


def SingletState(switch_phase: bool=False) -> Gate:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)
    if switch_phase:
        qc.z(1)
    return qc.to_gate()
