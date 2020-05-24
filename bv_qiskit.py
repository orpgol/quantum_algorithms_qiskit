import numpy as np

from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

import argparse, sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--s', help = 'Enter the secret string.')


class Bernstein_Vazirani(object):
	def __init__(self, n, s):
		self.n = n
		self.s = s

	def _run_bv(self):
		bv_circuit = QuantumCircuit(self.n+1,self.n)

		bv_circuit.h(self.n)
		bv_circuit.z(self.n) 

		for i in range(self.n):
		    bv_circuit.h(i)
		    
		s = self.s[::-1]
		for q in range(self.n):
		    if s[q] == '0':
		        bv_circuit.i(q)
		    else:
		        bv_circuit.cx(q, self.n)
		        
		for i in range(self.n):
		    bv_circuit.h(i)

		for i in range(self.n):
		    bv_circuit.measure(i, i)

		backend = BasicAer.get_backend('qasm_simulator')
		shots = 1024
		results = execute(bv_circuit, backend=backend, shots=shots).result()
		answer = results.get_counts()
		return answer

if __name__ == '__main__':
	start_time = time.time()
	args = parser.parse_args()
	s = args.s
	for i in s:
		if i != '0' and i != '1':
			raise AssertionError("s must be a bitstring")
	n = len(s)
	bv = Bernstein_Vazirani(n, s)
	answer = bv._run_bv()
	print(answer)
	print("--%s seconds--" % (time.time() - start_time))