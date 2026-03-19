
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from qalgo.qft import QuantumFourierTransformGate


def test_2qubit_qft_1():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(QuantumFourierTransformGate(2), [qr[0], qr[1]])

    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 1., 1., 1.]) * 0.5
    )


def test_2qubit_qft_2():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)    # a singlet state at this point
    singlet_statevector = Statevector(qc)

    # apply QFT gate
    qc.append(QuantumFourierTransformGate(2), [qr[0], qr[1]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        singlet_statevector.data,
        np.array([0., 1., 1., 0.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array([1., -0.5+0.5j, 0., -0.5-0.5j]) * np.sqrt(0.5)
    )

