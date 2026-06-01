from typing import Annotated

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from qiskit.circuit.library import StatePreparation, HamiltonianGate, RYGate

from .phase import PhaseEstimationGate, InversePhaseEstimationGate


def HHLGate(
        A: Annotated[npt.NDArray[np.float64], "2D Hermitian matrix"],
        b: Annotated[npt.NDArray[np.float64], "1D array"],
        nb_b: int,
        nb_clock: int,
        nb_ancilla: int = 1,
        time: float | np.float64 | None = None
) -> Gate:
    assert nb_ancilla == 1
    np.testing.assert_array_almost_equal(A, A.conj().T)

    eigenvalues = np.linalg.eigvalsh(A)
    pos_eigs = eigenvalues[eigenvalues > 1e-10]

    # Choose time so the largest eigenvalue maps to k = 2^(nb_clock-1),
    # ensuring exact QPE encoding when eigenvalues are rational multiples of λ_max/2^(nb_clock-1).
    if time is None:
        time = np.pi / float(np.max(pos_eigs))

    b_register = QuantumRegister(nb_b)
    clock_register = QuantumRegister(nb_clock)
    ancilla_register = QuantumRegister(nb_ancilla)
    qc = QuantumCircuit(ancilla_register, clock_register, b_register)

    qc.append(StatePreparation(b), [b_register[i] for i in range(nb_b)])

    evolution_gate = HamiltonianGate(A, time=time)

    qc.append(
        PhaseEstimationGate(evolution_gate, nb_clock, nb_b),
        [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )

    # Controlled reciprocal rotation.
    # HamiltonianGate gives e^{-iAt}, so eigenvalue λ > 0 produces phase φ = 1 − λt/(2π),
    # encoded as integer k = n_states − λ·t_scale  →  λ_k = (n_states − k) / t_scale.
    # For each k, rotate ancilla by 2·arcsin(C/λ_k) so that post-selecting ancilla=1
    # leaves the b register proportional to A^{-1}b.
    n_states = 2 ** nb_clock
    t_scale = time * n_states / (2 * np.pi)
    C = float(np.min(pos_eigs))

    for k in range(1, n_states):
        lambda_k = (n_states - k) / t_scale
        if lambda_k <= 0:
            continue
        theta = 2 * np.arcsin(min(C / lambda_k, 1.0))
        if abs(theta) < 1e-10:
            continue

        # clock_register[i] holds bit i of k (LSB-first / little-endian after QPE).
        # X-flip the 0-bits so the multi-controlled RY fires exactly when clock == |k⟩.
        k_bits = [(k >> i) & 1 for i in range(nb_clock)]

        for i in range(nb_clock):
            if k_bits[i] == 0:
                qc.x(clock_register[i])

        qc.append(
            RYGate(theta).control(nb_clock),
            [clock_register[i] for i in range(nb_clock)] + [ancilla_register[0]]
        )

        for i in range(nb_clock):
            if k_bits[i] == 0:
                qc.x(clock_register[i])

    qc.append(
        InversePhaseEstimationGate(evolution_gate.inverse(), nb_clock, nb_b),
        [clock_register[i] for i in range(nb_clock)] + [b_register[i] for i in range(nb_b)]
    )

    return qc.to_gate()
