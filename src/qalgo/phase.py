
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
# from qiskit.circuit.library import QFTGate

from .qft import QuantumFourierTransformGate


def PhaseEstimationGate(oracle_gate: Gate, nbphasedigits: int, nbstatequbits: int) -> Gate:
    controlled_oracle_gate = oracle_gate.control(1)

    phase_qregisters = QuantumRegister(nbphasedigits)
    state_qregisters = QuantumRegister(nbstatequbits)
    qc = QuantumCircuit(phase_qregisters, state_qregisters)
    qc.h(phase_qregisters)
    repetitions = 1
    for i in range(nbphasedigits):
        qc.append(
            controlled_oracle_gate.power(repetitions),
            [phase_qregisters[i]] + [state_qregisters[j] for j in range(nbstatequbits)]
        )
        repetitions *= 2

    qc.append(
        QuantumFourierTransformGate(phase_qregisters.size, inverse=True),
        [phase_qregisters[i] for i in range(nbphasedigits)]
    )
    # qc.append(
    #     QFTGate(phase_qregisters.size).inverse(True),
    #     [phase_qregisters[i] for i in range(nbphasedigits)]
    # )
    return qc.to_gate()
