# quantum_algorithms_qiskit

# Usage
In order to run these programs you must have Python 3 and Qiskit 2 properly installed.

## Bernstein-Vazirani
```
usage: bv_qiskit.py [-h] [--s S]

optional arguments:
  -h, --help  show this help message and exit
  --s S       Enter the secret string.
```

Example:

`python bv_qiskit.py 101`

Output:

Original `a` and `b`.

## Deutsch-Jozsa
```
usage: dj_qiskit.py [-h] [--bits BITS] [--algo ALGO]

optional arguments:
  -h, --help   show this help message and exit
  --bits BITS  Enter the number of bits you want to run with.
  --algo ALGO  Enter either "constant" or "balanced".
```

Examples:

`python dj_qiskit.py 3 balanced`

`python dj_qiskit.py 3 const`

Output:

Measurements for `n` bits (1 if the oracle is constant and 0 if it is balanced).

## Simon's
```
usage: simons.py [-h] string ftype

positional arguments:
  string      Secret string s of length n
  ftype       1 for one-to-one or 2 for two-to-one

optional arguments:
  -h, --help  show this help message and exit
```

Examples:

`python simons.py 10 1`

`python simons.py 100 2`

Output:

Prints statement indicating if the functions is one-to-one or two-to-one as well as the original secret string if the function is two-to-one.

## Grover
```
usage: grover.py [-h] [--bit BIT] [--valid VALID]

optional arguments:
  -h, --help     show this help message and exit
  --bit BIT      Enter the bit string for your function to search for
  --valid VALID  Enter valid for valid grover mapping or invalid for no string returning 1
```

Examples:

`python grover.py 101 valid`

`python grover.py 101 invalid`

Output:

The bitstring that returns 1 if the oracle is valid or a random bitstring if the oracle is invalid.

