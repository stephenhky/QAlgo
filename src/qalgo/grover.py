
from math import floor, pi, sqrt

from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate


class WrongQubitNumberException(Exception):
    pass


def GroverDiffusionGate(oracle_gate: Gate, nb_state_qubits: int) -> Gate:
    state_register = QuantumRegister(nb_state_qubits)
    ancilla_register = QuantumRegister(1)

    qc = QuantumCircuit(state_register, ancilla_register)

    if oracle_gate.num_qubits == nb_state_qubits:   # phase oracle
        qc.append(oracle_gate, [state_register[i] for i in range(nb_state_qubits)])
    elif oracle_gate.num_qubits == nb_state_qubits + 1:   # boolean oracle
        qc.append(oracle_gate)
    else:
        raise WrongQubitNumberException()

    qc.h(state_register)
    qc.mcx([state_register[i] for i in range(nb_state_qubits-1)], state_register[nb_state_qubits-1])
    qc.h(state_register)

    return qc.to_gate()


def GroverSearcher(oracle_gate: Gate, nb_state_qubits: int) -> Gate:
    state_register = QuantumRegister(nb_state_qubits, 'state')
    ancilla_register = QuantumRegister(1, 'ancilla')

    qc = QuantumCircuit(state_register, ancilla_register)

    # state preparation
    qc.h(state_register)
    qc.x(ancilla_register)
    qc.h(ancilla_register)

    nb_iters = floor(0.25 * pi * sqrt(nb_state_qubits))
    for _ in range(nb_iters):
        qc.append(
            GroverDiffusionGate(oracle_gate, nb_state_qubits),
            [state_register[i] for i in range(nb_state_qubits)] + [ancilla_register]
        )

    return qc.to_gate()
