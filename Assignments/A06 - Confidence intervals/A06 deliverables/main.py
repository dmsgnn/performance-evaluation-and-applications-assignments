# A06 - Giovanni Demasi, 10656704

import numpy as np
import math
from scipy.stats import norm

if __name__ == '__main__':
    nA = 50000
    nC = nA
    nAi = nA - 1
    interAi = []    # arrival times
    Si = []         # service times

    # Service times generation
    a = 5
    b = 10
    for i in range(0, nA):
        Si.append(np.random.uniform(low=a, high=b))

    # Inter-arrival times generation
    p1 = 0.1
    l1 = 0.02
    l2 = 0.2
    for i in range(0, nAi):
        if np.random.uniform(low=0, high=1) < p1:
            interAi.append(- math.log(np.random.uniform(low=0, high=1)) / l1)
        else:
            interAi.append(- math.log(np.random.uniform(low=0, high=1)) / l2)

    # computation of the arrival times, given the inter arrivals
    Ai = [0]  # assuming that the arrival time of the first request is at time 0
    for i in range(0, nAi):
        Ai.append(Ai[i] + interAi[i])

    # computation of the completion times
    Ci = [Ai[0] + Si[0]]
    for i in range(1, nA):
        Ci.append(max(Ai[i], Ci[i - 1]) + Si[i])

    # computation of the response times
    Ri = []
    for i in range(0, nA):
        Ri.append(Ci[i] - Ai[i])

    # average Response time per request, in seconds
    R = sum(Ri) / len(Ri)

    # estimation of the variance of the response times
    s2 = (1 / (nA - 1)) * np.sum(np.power(np.subtract(Ri, R), 2))

    gamma = 0.95  # confidence level

    # use of uniform, since nA > 30
    cgn = norm.ppf((1 + gamma) / 2)

    # upper and lower bound of R
    lowerR = R - cgn * math.sqrt(s2 / nA)
    upperR = R + cgn * math.sqrt(s2 / nA)

    k = 200  # number of runs
    m = 250  # number of jobs per each run

    Bi = []     # busy times of each run
    Ti = []     # observation time of each run
    Ui = []     # utilization of each run
    Xi = []     # throughput of each run
    Ni = []     # average number of jobs of each run
    for i in range(0, k):
        Bi.append(np.sum(Si[0 + (m * i): (m - 1) + (m * i)]))
        Ti.append(Ci[(m - 1) + (m * i)] - Ai[0 + (m * i)])
        Ui.append(Bi[i] / Ti[i])
        Xi.append(m / Ti[i])
        Ni.append(np.sum(Ri[0 + (m * i): (m - 1) + (m * i)]) / Ti[i])

    # Utilization
    U = np.sum(Ui) / len(Ui)
    # estimation of the variance of the utilization
    s2 = (1 / (k - 1)) * np.sum(np.power(np.subtract(Ui, U), 2))
    # upper and lower bound of U
    lowerU = U - cgn * math.sqrt(s2 / k)
    upperU = U + cgn * math.sqrt(s2 / k)

    # Throughput
    X = np.sum(Xi) / len(Xi)
    # estimation of the variance of the utilization
    s2 = (1 / (k - 1)) * np.sum(np.power(np.subtract(Xi, X), 2))
    # upper and lower bound of R
    lowerX = X - cgn * math.sqrt(s2 / k)
    upperX = X + cgn * math.sqrt(s2 / k)

    # Number of jobs
    N = np.sum(Ni) / len(Ni)
    # estimation of the variance of the utilization
    s2 = (1 / (k - 1)) * np.sum(np.power(np.subtract(Ni, N), 2))
    # upper and lower bound of R
    lowerN = N - cgn * math.sqrt(s2 / k)
    upperN = N + cgn * math.sqrt(s2 / k)

    print("> R")
    print("lower bound = " + f'{lowerR :.4f}')
    print("upper bound = " + f'{upperR :.4f}')
    print("> U")
    print("lower bound = " + f'{lowerU :.4f}')
    print("upper bound = " + f'{upperU :.4f}')
    print("> X")
    print("lower bound = " + f'{lowerX :.4f}')
    print("upper bound = " + f'{upperX :.4f}')
    print("> N")
    print("lower bound = " + f'{lowerN :.4f}')
    print("upper bound = " + f'{upperN :.4f}')
