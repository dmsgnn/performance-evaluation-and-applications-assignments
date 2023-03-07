# A11 - Giovanni Demasi, 10656704

import numpy as np
from math import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

if __name__ == '__main__':

    N = 16

    l = 200  # packets / second
    m = 100  # packets / second
    N0 = 8   # packets

    pn = [0]
    pd = [0]

    for i in range(1, N):
        if i < N0:
            lim = l
        else:
            lim = l * (N - i) / (N - N0)
        mi = m
        pn.append(pn[i - 1] + log(lim))
        pd.append(pd[i - 1] + log(mi))

        p = np.exp(np.subtract(pn, pd))
        p = np.divide(p, np.sum(p))

    for i in range(0, int(N / 2)):
        print("p" + str(i + 1) + " = " + f'{p[i] :.4f}' + "          " + "p" + str(
            i + int(N / 2) + 1) + " = " + f'{p[i + int(N / 2)] :.4f}')

    plt.plot(np.linspace(0, N, N), p, color="orange")
    plt.xlabel("Buffer occupation")
    plt.ylabel("p(n)")
    plt.title("Buffer occupation distribution")
    plt.show()
