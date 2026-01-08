
from qiskit.circuit import QuantumCircuit
from qiskit import transpile
from qiskit_aer import StatevectorSimulator

from qalgo.random import perfect_coin_gate


def test_perfect_coin() -> None:
    qc = QuantumCircuit(1, 1)
    qc.append(perfect_coin_gate())
    transpiled_qc = transpile(qc)

    simulator = StatevectorSimulator()
    simulation_results = simulator.run(transpiled_qc)
