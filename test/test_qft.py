
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit_aer import StatevectorSimulator

from qalgo.qft import QuantumFourierTransformGate


def test_2qubit_qft():
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    qc = QuantumCircuit(qr, cr)
    qc.append(QuantumFourierTransformGate(2), [qr[0], qr[1]])
    qc.measure(qr, cr)

    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(qc)

    assert count_dict.get("00", 0) > count_dict.get("10", 0)
    assert count_dict.get("00", 0) > count_dict.get("01", 0)
    assert count_dict.get("00", 0) > count_dict.get("11", 0)
