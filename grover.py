#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
#IBMQ.save_account('<your acct number>')

provider = IBMQ.load_account()

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
        self.qubits = None
        self.bit_map = None
        self.num_iter = None
            
    def _run_init(self, bit):
        self.bit_map = bit
        self.qubits = list(range(len(list(bit.keys())[0])))
        self.num_iter = int(round(np.sqrt(len(self.qubits))))

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
        
    def grover_run(self, bit, real=False):
        self._run_init(bit)
        
        oracle_matrix = self._grover_oracle_matrix(bit)
        oracle = Operator(oracle_matrix)
    
        diffusion_matrix = self._grover_diffusion_op()
        diffusion = Operator(diffusion_matrix)
        circuit = QuantumCircuit(len(self.qubits), len(self.qubits))
        circuit.h(self.qubits)
        ## Repeating part of the algorithm
        for _ in range(self.num_iter):
            circuit.append(oracle, self.qubits)
            circuit.h(self.qubits)
            circuit.append(diffusion, self.qubits)
            circuit.h(self.qubits)
            
        circuit.measure(self.qubits, self.qubits)
        
        if not real:
            # run the program on a QVM
            simulator = Aer.get_backend('qasm_simulator')
            job = execute(circuit, simulator, shots=1000)
        else:
            backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= len(self.qubits) and 
                                   not x.configuration().simulator and x.status().operational==True))
            
            print("least busy backend: ", backend)
            shots = 1024
            job = execute(circuit, backend=backend, shots=shots, optimization_level=3)

            job_monitor(job, interval = 2)
        
        # Grab results from the job
        try:
            result = job.result()
        except:
            print(job.error_message())
            return -1,-1
        # Returns counts
        counts = result.get_counts(circuit)
        print("\nTotal counts are:",counts)
        # Draw the circuit
        print(circuit.draw())
        print("Time taken:", result.time_taken)
        return circuit, result


# In[3]:


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
    circ, result = grover.grover_run(bit, real=True)


# In[ ]:




