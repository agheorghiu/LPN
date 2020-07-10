import qsharp
import math
from lpnETCF import clawFreeLPN
from helpers import *

# create an LPN instance
# takes m and n and returns a random m x n binary matrix A and a secret n-dimensional vector s
# randomness is initialized with a given seed
def createLPNinstance(seed: int, m: int, n: int) -> (List[List[int]], List[int]):
    np.random.seed(seed)
    A = np.random.randint(2, size=[m, n])
    s = np.random.randint(2, size=[n, 1])
    return (A, s)

# create m-dimensional binary error vector
# probability of error is p
def createErrVector(seed: int, m: int, p: float) -> List[int]:
    np.random.seed(seed)
    e = np.zeros([m, 1], dtype=int)
    for i in range(m):
        rand = np.random.rand()
        if (p >= rand):
            e[i] = 1
    return e

# parameters
seed = 1339
n = 8
m = 2 * n
p = 0.04

A, s = createLPNinstance(seed, m, n)
e = createErrVector(seed, m, 0.04)
lpnInstance = (np.dot(A, s) + e) % 2


res = clawFreeLPN.simulate(A=A.tolist(), lpnInstance=(list (map(lambda x: x[0], lpnInstance.tolist()))), p=p)

print("")
print("---------------------------------------------------------------------------------")
print(A)
print(s)
print(lpnInstance)
print(e)
print(res)

print(sum(sum(A)) + sum(sum(lpnInstance)) + 1)

# print(computeRank(A))