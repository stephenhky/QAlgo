
import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import StatevectorSimulator
from loguru import logger

from qalgo.hhl import HHLGate


def test_hhl_1():
    A = np.array([[1., -np.reciprocal(3.)], [-np.reciprocal(3.), 1.]])
    b = np.array([0., 1.])

    nb_b = 1
    nb_clock = 4

    ancilla_register = QuantumRegister(1)
    clock_register = QuantumRegister(nb_clock)
    b_register = QuantumRegister(nb_b)
    classical_register = ClassicalRegister(1)
    qc = QuantumCircuit(ancilla_register, clock_register, b_register, classical_register)
    qc.append(
        HHLGate(A, b, nb_b, nb_clock),
        [ancilla_register[0]] + [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )
    qc.measure(ancilla_register[0], classical_register)

    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(qc)

    logger.info(count_dict)
