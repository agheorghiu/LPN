import functools
import numpy as np
from typing import *
from scipy.linalg import null_space

# Create reduced row-echelon form
def rregf2(lst: List[List[int]]) -> np.ndarray:
    # convert everything to int and make it a numpy array
    mat = np.array(lst)
    m, n = mat.shape
    i, j = 0, 0
    while i < m and j < n:
        # find value and index of largest element in remainder of column j
        k = np.argmax(mat[i:, j]) + i

        if (mat[k, j] == 0):
            mat[i:, j] = 0
            j += 1
        else:
            # Swap i-th and k-th rows.
            mat[[k, i], j:] = mat[[i, k], j:]

            # current row
            row = np.copy(mat[i, j:])

            # add pivot mod 2 to all rows
            mat[:, j:] = (mat[:, j:] + np.outer(mat[:, j], row)) % 2

            # restore row
            mat[i, j:] = row

            i += 1
            j += 1
    return mat

# compute rank of binary matrix
def computeRank(lst: List[List[int]]) -> int:
    reduced = rregf2(lst)
    return np.linalg.matrix_rank(reduced)