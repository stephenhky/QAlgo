
from operator import itemgetter

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import TGate
from qiskit import transpile
from qiskit_aer import StatevectorSimulator

from qalgo.phase import PhaseEstimationGate


def test_phase_T0():
    phase_register = QuantumRegister(4)
    state_register = QuantumRegister(1)
    classical_register = ClassicalRegister(4)

    quantum_circuit = QuantumCircuit(phase_register, state_register, classical_register)
    quantum_circuit.append(
        PhaseEstimationGate(TGate(), 4, 1),
        [phase_register[0], phase_register[1], phase_register[2], phase_register[3], state_register[0]]
    )
    quantum_circuit.measure(phase_register, classical_register)

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(quantum_circuit, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(quantum_circuit)

    # statistics test
    print(count_dict)
    greatest_state_count = max(count_dict.items(), key=itemgetter(1))
    assert greatest_state_count[0] == "0000"


def test_phase_T1():
    phase_register = QuantumRegister(4)
    state_register = QuantumRegister(1)
    classical_register = ClassicalRegister(4)

    quantum_circuit = QuantumCircuit(phase_register, state_register, classical_register)
    quantum_circuit.x(state_register[0])
    quantum_circuit.append(
        PhaseEstimationGate(TGate(), 4, 1),
        [phase_register[0], phase_register[1], phase_register[2], phase_register[3], state_register[0]]
    )
    quantum_circuit.measure(phase_register, classical_register)

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(quantum_circuit, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(quantum_circuit)

    # statistics test
    print(count_dict)
    greatest_state_count = max(count_dict.items(), key=itemgetter(1))
    assert greatest_state_count[0] == "0010"
