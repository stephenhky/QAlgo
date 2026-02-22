
from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister


def PerfectCoinGate() -> Gate:
    qr = QuantumRegister(1)
    qc = QuantumCircuit(qr)
    qc.h(qr[0])
    return qc.to_gate()
