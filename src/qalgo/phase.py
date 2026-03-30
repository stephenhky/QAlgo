
import numpy as np
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister, Gate


def PhaseEstimationGate(nbphasedigits: int, nbstatequbits: int) -> Gate:
    phase_qregisters = QuantumRegister(nbphasedigits)
    state_qregisters = QuantumRegister(nbstatequbits)
    cregisters = ClassicalRegister(nbphasedigits)
    qc = QuantumCircuit(phase_qregisters, state_qregisters, cregisters)
    qc.h([phase_qregisters[i] for i in range(phase_qregisters.size)])
    for i in range(nbphasedigits):
        qc.cu(0., 0., np.pi * (2**i), 0., phase_qregisters[i],
              [state_qregisters[j] for j in range(nbstatequbits)])

