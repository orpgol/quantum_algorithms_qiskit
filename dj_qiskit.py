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


class Deutsch_Jozsa(object):
    def __init__(self, n, algo):
        self.n = n
        self.algo = algo

    #change to self
    def _dj_oracle(self):
        oracle_qc = QuantumCircuit(self.n+1)
        
        if self.algo == "balanced":
            b = np.random.randint(1,2**self.n)
            b_str = format(b, '0'+str(self.n)+'b')
            for qubit in range(len(b_str)):
                if b_str[qubit] == '1':
                    oracle_qc.x(qubit)
            for qubit in range(self.n):
                oracle_qc.cx(qubit, self.n)
            for qubit in range(len(b_str)):
                if b_str[qubit] == '1':
                    oracle_qc.x(qubit)

        if self.algo == "constant":
            output = np.random.randint(2)
            if output == 1:
                oracle_qc.x(self.n)
        
        return oracle_qc.to_gate()

    def _dj_algorithm(self, oracle):
        dj_circuit = QuantumCircuit(self.n+1, self.n)
        dj_circuit.x(self.n)
        dj_circuit.h(self.n)
        
        for qubit in range(self.n):
            dj_circuit.h(qubit)
        dj_circuit.append(oracle, range(n+1))
        for qubit in range(self.n):
            dj_circuit.h(qubit)
        for i in range(self.n):
            dj_circuit.measure(i, i)
        
        results = execute(dj_circuit, backend=backend, shots=1024).result()
        answer = results.get_counts()
        print(answer)
        print("--%s seconds--" % (time.time() - start_time))

if __name__ == '__main__':
    start_time = time.time()
    backend = BasicAer.get_backend('qasm_simulator')
    args = parser.parse_args()
    n = int((args.bits))

    if n < 1:
        raise AssertionError("n must be a number of bits greater than 0")
    if args.algo != ('constant') and args.algo != ('balanced'):
        raise AssertionError("algo must be either balanced or constant")

    dj = Deutsch_Jozsa(n, args.algo)
    oracle_gate = dj._dj_oracle()
    dj_circuit = dj._dj_algorithm(oracle_gate)

	