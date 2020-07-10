# LPN

## lpn.py

Contains an implementation of a claw-free function based on Learning Parities with Noise (LPN) instead of LWE. Specifically, the function is

f(b, x) = Ax + b.(As + e) + e'

Where A is an m x n binary matrix, s is an n-dimensional binary vector, and e and e' are m-dimensional binary vectors. For both e and e' the entries are chosen i.i.d. from a Bernoulli random variable with probability p.

If the matrix used in LPN is m x n, the depth of the resulting circuit will be |A| + |As + e| + 1 ≤ mn + m + 1, where |.| denotes Hamming weight and As + e is the LPN instance.

## Operations.qs

Contains the Q# implementation of evaluating CF function based on LPN.

## binDist.py

Contains code for computing overlap/distance between a binomial distribution over error vectors and its shifted version. Also computes overlap between uniform distribution (over low weight error vectors) and its shifted version.
Some results are in the `plots` folder.

## helpers.py

Some helper functions.
