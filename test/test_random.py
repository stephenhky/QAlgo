
from qiskit.circuit import QuantumCircuit

from qalgo.random import perfect_coin_gate


def test_perfect_coin() -> None:
    qc = QuantumCircuit(1, 1)
    qc.append(perfect_coin_gate())



