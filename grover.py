#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.compiler import transpile
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.quantum_info import process_fidelity

from qiskit.extensions import RXGate, XGate, CXGate

from qiskit.visualization import plot_histogram

from collections import defaultdict
import pprint
import argparse, sys

parser=argparse.ArgumentParser()
parser.add_argument('--bit', help='Enter the bit string for your function to search for')
parser.add_argument('--valid', help='Enter valid for valid grover mapping or invalid for no string returning 1')


# In[2]:


def create_grover_valid_bitmap(bit):
    n_bits = len(bit)
    bit_map = {}
    for bit_val in range(2 ** n_bits):
        if(np.binary_repr(bit_val, width=n_bits) == bit):
            bit_map[np.binary_repr(bit_val, width=n_bits)] = str(1)
        else:
            bit_map[np.binary_repr(bit_val, width=n_bits)] = str(0)

    return bit_map

def create_grover_invalid_bitmap(bit):
    n_bits = len(bit)
    bit_map = {}
    for bit_val in range(2 ** n_bits):
        bit_map[np.binary_repr(bit_val, width=n_bits)] = str(0)

    return bit_map

class Grover(object):
    def _init_(self):        
        self.n_qubits = None
        self.qubits = None
        self.bit_map = None
        self.num_iter = None
            
    def _run_init(self, bit):
        self.bit_map = bit
        self.n_qubits = 2**len(list(bit.keys())[0])
        self.qubits = list(range(int(np.log2(self.n_qubits))))
        self.num_iter = int(round(np.pi * 2 ** (len(self.qubits) / 2.0 - 2.0)))

    def _grover_oracle_matrix(self, bit):
        n_bits = len(list(bit.keys())[0])
        oracle_matrix = np.zeros(shape=(2 ** n_bits, 2 ** n_bits))
        for b in range(2 ** n_bits):
            bin_str = np.binary_repr(b, n_bits)
            fill_value = bit[bin_str]
            if fill_value == '0': fill_value = '-1'
            oracle_matrix[b, b] = fill_value
        return oracle_matrix
    
    def _grover_diffusion_op(self):
        dim = 2 ** len(self.qubits)
        diffusion_matrix = np.diag([1.0] + [-1.0] * (dim - 1))
        return diffusion_matrix
        
    def grover_run(self, bit):
        self._run_init(bit)
        
        oracle_matrix = self._grover_oracle_matrix(bit)
        oracle = Operator(oracle_matrix)
    
        diffusion_matrix = self._grover_diffusion_op()
        diffusion = Operator(diffusion_matrix)

        simulator = Aer.get_backend('qasm_simulator')
        circuit = QuantumCircuit(len(self.qubits), len(self.qubits))
        circuit.h(self.qubits)
        ## Repeating part of the algorithm
        for _ in range(self.num_iter):
            circuit.append(oracle, self.qubits)
            circuit.h(self.qubits)
            circuit.append(diffusion, self.qubits)
            circuit.h(self.qubits)
            
        circuit.measure(self.qubits, self.qubits)
        # run the program on a QVM
        job = execute(circuit, simulator, shots=1000)
        # Grab results from the job
        result = job.result()
        # Returns counts
        counts = result.get_counts(circuit)
        print("\nTotal count for 00 and 11 are:",counts)
        # Draw the circuit
        print(circuit.draw())


# In[ ]:


if __name__ == '__main__':
    args=parser.parse_args()
    
    ## Assert bit string
    p = set(args.bit)
    s = {'0','1'}
    if s == p or p == {'0'} or p == {'1'}:
    #     print('ok')
        pass
    else:
        raise AssertionError("bit must be a bit strings")
        
    if args.valid == 'valid':
        bit = create_grover_valid_bitmap(args.bit)
    elif args.valid == 'invalid':
        bit = create_grover_invalid_bitmap(args.bit)
    else:
        raise AssertionError("valid must be a either 'valid' or 'invalid' strings")
        
    grover = Grover()
    grover.grover_run(bit)

