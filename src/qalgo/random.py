
from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister, ClassicalRegister

def perfect_coin_gate() -> Gate:
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)

    qc.h(qr[0])
    qc.measure(qr, cr)

    return qc.to_gate()
