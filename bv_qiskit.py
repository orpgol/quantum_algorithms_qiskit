import numpy as np

from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('--s', help = 'Enter the secret string.')

def run_bv(n, s):
	bv_circuit = QuantumCircuit(n+1, n)

	bv_circuit.h(n)
	bv_circuit.z(n) 

	for i in range(n):
	    bv_circuit.h(i)
	    
	s = s[::-1]
	for q in range(n):
	    if s[q] == '0':
	        bv_circuit.i(q)
	    else:
	        bv_circuit.cx(q, n)
	        
	for i in range(n):
	    bv_circuit.h(i)

	for i in range(n):
	    bv_circuit.measure(i, i)

	backend = BasicAer.get_backend('qasm_simulator')
	shots = 1024
	results = execute(bv_circuit, backend=backend, shots=shots).result()
	answer = results.get_counts()
	return answer

if __name__ == '__main__':
	args = parser.parse_args()
	s = args.s
	n = len(s)
	answer = run_bv(n, s)
	print(answer)
