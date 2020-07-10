from typing import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
import math
import imageio

# converting between binary and int
def toBinary(num: int, numBits: int) -> List[int]:
    return list(reversed([int((num & (2**i)) > 0) for i in range(numBits)]))

# add binary strings
def binAdd(x: List[int], y: List[int]) -> List[int]:
    return [((a + b) % 2) for (a, b) in zip(x, y)]

# probability of a specific string in the binomial case
def binProb(p: float, x: List[int]) -> int:
    n = len(x)
    hamw = sum(x)
    return (p ** hamw) * (1 - p) ** (n - hamw)

# probability of a specific string in the uniform case
def unifProb(thresh: int, x: List[int]) -> int:
    n = len(x)
    hamw = sum(x)
    if (hamw > thresh):
        return 0
    numStrings = 0
    for i in range(thresh + 1):
        numStrings += sp.binom(n, i)
    return 1 / numStrings

# distance between binomial distribution and its shifted version
def distBin(thresh: float, n: int, shift: List[int]) -> float:
    overlap = 0
    for i in range(0, 2 ** n - 1):
        x = toBinary(i, n)
        probX = binProb(p, x)
        probShift = binProb(p, binAdd(x, shift))
        overlap += math.sqrt(probX * probShift)
    return (1 - overlap)

# distance between uniform distribution and its shifted version
def distUnif(thresh: int, n: int, shift: List[int]) -> float:
    overlap = 0
    for i in range(0, 2 ** n - 1):
        x = toBinary(i, n)
        probX = unifProb(thresh, x)
        probShift = unifProb(thresh, binAdd(x, shift))
        overlap += math.sqrt(probX * probShift)
    return (1 - overlap)

# create n-bit string having a given Hamming weight
def createWeightedString(n: int, weight: int) -> List[int]:
    return toBinary(2 ** weight - 1, n)

#binomial case

# # fix n and try a bunch of different values for p
# # plot distances/overlap for all Hamming weights of shift
# n = 15

# images = []
# for p in np.arange(0.00, 0.55, 0.05):
#     # compute overlap between distributions for all possible shifts
#     vals = np.array(list(map(lambda w: 1 - distBin(p, n, createWeightedString(n, w)), range(0, n + 1))))
#     y_pos = np.arange(len(vals))

#     # create plot of overlaps
#     plt.bar(y_pos, vals, align='center', alpha=0.5)
#     plt.xticks(y_pos, range(0, len(vals)))
#     plt.ylabel('Overlap')
#     plt.xlabel('Hamming weight of shift')
#     plt.title('Overlap between binomial and its shifted version \n n=' + str(n) + '    ' + 'p=' + '{:01.2f}'.format(p))

#     # save plot to file
#     filename = 'plots/n=' + str(n) + '_p={:02.0f}.jpg'.format(p * 100)
#     plt.savefig(filename)
#     plt.close()

#     # collect images to create animated gif
#     images.append(imageio.imread(filename))

# # make gif of plots
# imageio.mimsave('plots/n=' + str(n) + '_p_00_to_50.gif', images, duration=0.7)


# uniform case
n = 12

images = []
for thresh in range(0, n + 1):
    # compute overlap between distributions for all possible shifts
    vals = np.array(list(map(lambda w: 1 - distUnif(thresh, n, createWeightedString(n, w)), range(0, n + 1))))
    y_pos = np.arange(len(vals))

    # create plot of overlaps
    plt.bar(y_pos, vals, align='center', alpha=0.5)
    plt.xticks(y_pos, range(0, len(vals)))
    plt.ylabel('Overlap')
    plt.xlabel('Hamming weight of shift')
    plt.title('Overlap between uniform and its shifted version \n n=' + str(n) + '    ' + 'threshold=' + str(thresh))

    # save plot to file
    filename = 'plots/n=' + str(n) + '_th=' + str(thresh) + '.jpg'
    plt.savefig(filename)
    plt.close()

    # collect images to create animated gif
    images.append(imageio.imread(filename))

# make gif of plots
imageio.mimsave('plots/n=' + str(n) + '.gif', images, duration=0.7)