
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from qalgo.qft import QuantumFourierTransformGate


def test_2qubit_qft():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(QuantumFourierTransformGate(2), [qr[0], qr[1]])

    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 1., 1., 1.]) * 0.5
    )
