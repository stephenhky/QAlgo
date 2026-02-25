
from qiskit.circuit import QuantumRegister, QuantumCircuit, ClassicalRegister
from qiskit import transpile
from qiskit_aer import StatevectorSimulator
from qiskit.circuit.library import CZGate
from loguru import logger

from qalgo.grover import GroverSearcher


def test_grover_11():
    # define the oracle
    oracle_gate = CZGate()

    # build the circuit
    grover_searcher = GroverSearcher(oracle_gate, 2)
    state_registry = QuantumRegister(2)
    ancilla_register = QuantumRegister(1)
    classical_register = ClassicalRegister(2)
    qc = QuantumCircuit(state_registry, ancilla_register, classical_register)
    qc.append(
        grover_searcher,
        [state_registry[i] for i in range(2)] + [ancilla_register]
    )
    qc.measure(state_registry, classical_register)

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(qc)

    assert count_dict["011"] + count_dict["111"] > count_dict["000"] + count_dict["100"]
    assert count_dict["011"] + count_dict["111"] > count_dict["001"] + count_dict["101"]
    assert count_dict["011"] + count_dict["111"] > count_dict["010"] + count_dict["110"]
