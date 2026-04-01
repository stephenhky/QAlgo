
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import QFTGate

from qalgo.qft import QuantumFourierTransformGate
from qalgo.stateprep import GHZState


def test_2qubit_qft_1():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(QuantumFourierTransformGate(2), qr)

    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 1., 1., 1.]) * 0.5
    )


def test_2qubit_qiskitqftgate_1():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(QFTGate(2), qr)

    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 1., 1., 1.]) * 0.5
    )


def test_2qubit_inverseqft_1():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(QuantumFourierTransformGate(2), qr)

    statevector = Statevector(qc)
    np.testing.assert_array_almost_equal(
        statevector.data,
        np.array([1., 1., 1., 1.]) * 0.5
    )


def test_2qubit_qft_2():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(2), qr)   # a singlet state at this point
    singlet_statevector = Statevector(qc)

    # apply QFT gate
    qc.append(QuantumFourierTransformGate(2), qr)
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        singlet_statevector.data,
        np.array([0., 1., 1., 0.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array([1., -0.5+0.5j, 0., -0.5-0.5j]) * np.sqrt(0.5)
    )


def test_2qubit_qiskitqftgate_2():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(2), [qr[0], qr[1]])   # a singlet state at this point
    singlet_statevector = Statevector(qc)

    # apply the QFT gate
    qc.append(QFTGate(2), [qr[0], qr[1]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        singlet_statevector.data,
        np.array([0., 1., 1., 0.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array([1., -0.5 + 0.5j, 0., -0.5 - 0.5j]) * np.sqrt(0.5)
    )


def test_2qubit_inverseqft_2():
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(2), [qr[0], qr[1]])   # a singlet state at this point
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
        np.array([1., -0.5-0.5j, 0., -0.5+0.5j]) * np.sqrt(0.5)
    )


def test_2qubit_qft_3():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.append(QuantumFourierTransformGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.repeat(np.sqrt(0.125), 8)
    )


def test_2qubit_qiskitqft_3():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.append(QFTGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.repeat(np.sqrt(0.125), 8)
    )


def test_2qubit_qft_4():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.x(qr)    # |111>
    allone_statevector = Statevector(qc)

    qc.append(QuantumFourierTransformGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        allone_statevector.data,
        np.array([0., 0., 0., 0., 0., 0., 0., 1.])
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array([1., np.sqrt(0.5)*(1.-1.j), -1.j, -np.sqrt(0.5)*(1+1.j),
                  -1., np.sqrt(0.5)*(-1+1.j), 1.j, np.sqrt(0.5)*(1+1.j)]) * np.sqrt(0.125)
    )


def test_2qubit_qiskitqft_4():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.x(qr)    # |111>
    allone_statevector = Statevector(qc)

    qc.append(QFTGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        allone_statevector.data,
        np.array([0., 0., 0., 0., 0., 0., 0., 1.])
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array([1., np.sqrt(0.5)*(1.-1.j), -1.j, -np.sqrt(0.5)*(1+1.j),
                  -1., np.sqrt(0.5)*(-1+1.j), 1.j, np.sqrt(0.5)*(1+1.j)]) * np.sqrt(0.125)
    )


def test_2qubit_qft_5():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(3), [0, 1, 2])     # GHZ state
    ghz_statevector = Statevector(qc)

    qc.append(QuantumFourierTransformGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        ghz_statevector.data,
        np.array([1., 0., 0., 0., 0., 0., 0., 1.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array(
            [0.5, 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1-1.j), 0.25*(1.-1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1-1.j),
             0., 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1+1.j),  0.25*(1.+1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1+1.j)]
        )
    )


def test_2qubit_qiskitqft_5():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(3), [0, 1, 2])     # GHZ state
    ghz_statevector = Statevector(qc)

    qc.append(QFTGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        ghz_statevector.data,
        np.array([1., 0., 0., 0., 0., 0., 0., 1.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array(
            [0.5, 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1-1.j), 0.25*(1.-1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1-1.j),
             0., 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1+1.j),  0.25*(1.+1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1+1.j)]
        )
    )


def test_2qubit_inverseqft_5():
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.append(GHZState(3), [0, 1, 2])     # GHZ state
    ghz_statevector = Statevector(qc)

    qc.append(QuantumFourierTransformGate(3), [qr[0], qr[1], qr[2]])
    qft_statevector = Statevector(qc)

    np.testing.assert_array_almost_equal(
        ghz_statevector.data,
        np.array([1., 0., 0., 0., 0., 0., 0., 1.]) * np.sqrt(0.5)
    )
    np.testing.assert_array_almost_equal(
        qft_statevector.data,
        np.array(
            [0.5, 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1+1.j), 0.25*(1.+1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1+1.j),
             0., 0.25*np.sqrt(0.5)*(np.sqrt(2.)-1-1.j),  0.25*(1.-1.j), 0.25*np.sqrt(0.5)*(np.sqrt(2.)+1-1.j)]
        )
    )
