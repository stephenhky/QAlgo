
import numpy as np
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister, Gate

from .qft import QuantumFourierTransformGate


def PhaseEstimationGate(oracle_gate: Gate, nbphasedigits: int, nbstatequbits: int) -> Gate:
    controlled_oracle_gate = oracle_gate.control(1)

    phase_qregisters = QuantumRegister(nbphasedigits)
    state_qregisters = QuantumRegister(nbstatequbits)
    cregisters = ClassicalRegister(nbphasedigits)
    qc = QuantumCircuit(phase_qregisters, state_qregisters, cregisters)
    qc.h(phase_qregisters)
    for i in range(nbphasedigits):
        qc.append(
            controlled_oracle_gate.power(2**i),
            [phase_qregisters[i]] + [state_qregisters[j] for j in range(nbstatequbits)]
        )

    qc.append(QuantumFourierTransformGate(phase_qregisters.size), [phase_qregisters])

