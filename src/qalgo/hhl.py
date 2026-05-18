
from typing import Annotated

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from qiskit.circuit.library import StatePreparation, HamiltonianGate

from .phase import PhaseEstimationGate, InversePhaseEstimationGate


def HHLGate(
        A: Annotated[npt.NDArray[np.float64], "2D Hermitian matrix"],
        b: Annotated[npt.NDArray[np.float64], "1D array"],
        nb_b: int,   # b qubit
        nb_clock: int,   # clock qubit
        nb_ancilla: int = 1,    # ancilla qubit
        time: float | np.float64 = 2*np.pi/4
) -> Gate:
    assert nb_ancilla == 1     # ancilla must have only one qubit
    np.testing.assert_array_almost_equal(A, A.conj().T)   # test Hermitianity

    # initiating the circuit
    b_register = QuantumRegister(nb_b)
    clock_register = QuantumRegister(nb_clock)
    ancilla_register = QuantumRegister(nb_ancilla)
    qc = QuantumCircuit(ancilla_register, clock_register, b_register)

    # initiating b
    b_state_prep = StatePreparation(b)
    qc.append(b_state_prep, [b_register[i] for i in range(nb_b)])

    # initiating evolution gate
    evolution_gate = HamiltonianGate(A, time=time)

    # forward quantum phase estimation
    qc.append(
        PhaseEstimationGate(evolution_gate, nb_clock, nb_b),
        [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )

    # controlled rotation
    for i in range(nb_clock):
        qc.cry(np.pi / (2**i), [clock_register[i] for i in range(nb_clock)], ancilla_register[0])

    # reverse quantum phase estimation
    qc.append(
        InversePhaseEstimationGate(evolution_gate.inverse(), nb_clock, nb_b),
        [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )

    return qc.to_gate()
