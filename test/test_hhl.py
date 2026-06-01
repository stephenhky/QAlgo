
import numpy as np
import pytest
from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from qalgo.hhl import HHLGate


def test_hhl_1():
    A = np.array([[1., -np.reciprocal(3.)], [-np.reciprocal(3.), 1.]])
    b = np.array([0., 1.])

    nb_b = 1
    nb_clock = 4

    ancilla_register = QuantumRegister(1)
    clock_register = QuantumRegister(nb_clock)
    b_register = QuantumRegister(nb_b)
    qc = QuantumCircuit(ancilla_register, clock_register, b_register)
    qc.append(
        HHLGate(A, b, nb_b, nb_clock),
        [ancilla_register[0]] + [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )

    sv = Statevector(qc)
    filtered_probs = {
        str(key): float(prob)
        for key, prob in sv.probabilities_dict().items()
        if key[-1] == '1'
    }
    measured_b_proba = {
        "0": sum(val for key, val in filtered_probs.items() if key[0]=="0"),
        "1": sum(val for key, val in filtered_probs.items() if key[0]=="1")
    }
    assert measured_b_proba["1"] > measured_b_proba["0"]
    assert measured_b_proba["1"] / measured_b_proba["0"] == pytest.approx((9.))
