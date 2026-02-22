
from math import sqrt

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import StatevectorSimulator

from qalgo.random import PerfectCoinGate


def test_perfect_coin() -> None:
    # build the circuit
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)
    qc.append(PerfectCoinGate(), [qr[0]])
    qc.measure(qr[0], cr[0])

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(qc)

    # statistics test
    mean = nbshots * 0.5
    std = sqrt(nbshots * 0.5 * 0.5)
    assert mean - 3*std < count_dict['0'] < mean + 3*std
