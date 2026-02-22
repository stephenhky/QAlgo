
from qiskit.circuit import QuantumRegister, QuantumCircuit, ClassicalRegister, transpile
from qiskit_aer import StatevectorSimulator
from qiskit.circuit.library import CZGate

from qalgo.grover import GroverDiffusionGate, GroverSearcher


def test_grover_11():
    # define the oracle
    oracle_gate = CZGate()

    # build the circuit
    grover_searcher = GroverSearcher(oracle_gate, 2)
    state_registry = QuantumRegister(2)
    ancilla_register = QuantumRegister(1)
    classical_register = ClassicalRegister(2)
    qc = QuantumCircuit(state_registry, ancilla_register, classical_register)
    qc.append(grover_searcher, [state_registry, ancilla_register, classical_register])

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(qc)

    print(count_dict)
