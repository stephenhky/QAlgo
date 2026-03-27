
import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qalgo.stateprep import GHZState


def test_2qubit_ghz_state():
    qc = QuantumCircuit(2)
    qc.append(GHZState(2), [0, 1])
    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 0., 0., 1.]) * np.sqrt(0.5)
    )


def test_3qubit_ghz_state():
    qc = QuantumCircuit(3)
    qc.append(GHZState(3), [0, 1, 2])
    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 0., 0., 0., 0., 0., 0., 1.]) * np.sqrt(0.5)
    )


def test_4qubit_ghz_state():
    qc = QuantumCircuit(4)
    qc.append(GHZState(4), [0, 1, 2, 3])
    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 0., 0., 0.,
                  0., 0., 0., 0.,
                  0., 0., 0., 0.,
                  0., 0., 0., 1.]) * np.sqrt(0.5)
    )
