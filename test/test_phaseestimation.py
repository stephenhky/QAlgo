
from operator import itemgetter

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import TGate, phase_estimation
from qiskit.quantum_info import Statevector
from qiskit import transpile
from qiskit_aer import StatevectorSimulator
from loguru import logger

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
    phase_statevector = Statevector(quantum_circuit)
    quantum_circuit.measure(phase_register, classical_register)

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(quantum_circuit, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(quantum_circuit)

    # statistics test
    logger.info(phase_statevector.data)
    logger.info(count_dict)
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
    phase_statevector = Statevector(quantum_circuit)
    quantum_circuit.measure(phase_register, classical_register)

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(quantum_circuit, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(quantum_circuit)

    # statistics test
    logger.info(phase_statevector.data)
    logger.info(count_dict)
    greatest_state_count = max(count_dict.items(), key=itemgetter(1))
    assert greatest_state_count[0] == "0010"


def test_phase_T1_qiskit():
    # unitary gate
    t_gate_qcircuit = QuantumCircuit(1, name="T_Gate")
    t_gate_qcircuit.t(0)

    # state preparation
    state_prep = QuantumCircuit(1, name="eigenstate")
    state_prep.x(0)

    # phase estimation gate
    qpe_circuit = phase_estimation(num_evaluation_qubits=4, unitary=t_gate_qcircuit)

    # full circuit
    full_circuit = QuantumCircuit(4+1)
    full_circuit.compose(state_prep, qubits=[4], inplace=True)
    full_circuit.compose(qpe_circuit, inplace=True)

    # measurement
    full_circuit.measure_all()

    # simulation
    nbshots = 1024
    simulator = StatevectorSimulator(max_shot_size=1024)
    transpiled_qc = transpile(full_circuit, simulator, optimization_level=0)
    job = simulator.run(transpiled_qc, shots=nbshots)
    result = job.result()
    count_dict = result.get_counts(full_circuit)

    # statistics test
    logger.info(count_dict)
    greatest_state_count = max(count_dict.items(), key=itemgetter(1))
    assert greatest_state_count[0] == "10100"
