# quantum_algorithms_qiskit

# Usage
In order to run these programs you must have Python 3 and Qiskit 2 properly installed.

## Bernstein-Vazirani
```
usage: Bernstein-Vazirani.py [-h] a b

positional arguments:
  a           Enter the a bit string for the function ax(xor)b you want to run
              with
  b           Enter the b sibgle bit for the function ax(xor)b you want to run
              with

optional arguments:
  -h, --help  show this help message and exit
```

Example:

`python Bernstein-Vazirani.py 101 1`

Output:

Original `a` and `b`.

## Deutsch-Jozsa
```
usage: Deutsch-Jozsa.py [-h] bits algo

positional arguments:
  bits        Enter the number of bits you want to run with
  algo        Enter balanced for balanced or const for constant function

optional arguments:
  -h, --help  show this help message and exit
```

Examples:

`python Deutsch-Jozsa.py 3 balanced`

`python Deutsch-Jozsa.py 3 const`

Output:

Measurements for `n` bits (1 if the oracle is constant and 0 if it is balanced).

## Simon's
```
usage: Simons.py [-h] string ftype

positional arguments:
  string      Secret string s of length n
  ftype       1 for one-to-one or 2 for two-to-one

optional arguments:
  -h, --help  show this help message and exit
```

Examples:

`python Simons.py 10 1`

`python Simons.py 100 2`

Output:

Prints statement indicating if the functions is one-to-one or two-to-one as well as the original secret string if the function is two-to-one.

## Grover
```
usage: Grover.py [-h] bit valid

positional arguments:
  bit         Enter the bit string for your function to search for
  valid       Enter valid for valid grover mapping or invalid for no string
              returning 1

optional arguments:
  -h, --help  show this help message and exit
```

Examples:

`python Grover.py 101 valid`

`python Grover.py 101 invalid`

Output:

The bitstring that returns 1 if the oracle is valid or a random bitstring if the oracle is invalid.

