import numpy as np
from qiskit import BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_histogram
import argparse, sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--bits', help = 'Enter the number of bits you want to run with.')
parser.add_argument('--algo', help = 'Enter either "constant" or "balanced".')


def dj_oracle(algo, n):
    oracle_qc = QuantumCircuit(n+1)
    
    if algo == "balanced":
        b = np.random.randint(1,2**n)
        b_str = format(b, '0'+str(n)+'b')
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    if algo == "constant":
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)
    
    return oracle_qc.to_gate()


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)
    dj_circuit.x(n)
    dj_circuit.h(n)
    
    for qubit in range(n):
        dj_circuit.h(qubit)
    dj_circuit.append(oracle, range(n+1))
    for qubit in range(n):
        dj_circuit.h(qubit)
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit

if __name__ == '__main__':
	start_time = time.time()
	backend = BasicAer.get_backend('qasm_simulator')
	args = parser.parse_args()
	n = len((args.bits))
	oracle_gate = dj_oracle(args.algo, n)
	dj_circuit = dj_algorithm(oracle_gate, n)
	dj_circuit.draw()

	results = execute(dj_circuit, backend=backend, shots=1024).result()
	answer = results.get_counts()
	print(answer)
	print("--%s seconds--" % (time.time() - start_time))