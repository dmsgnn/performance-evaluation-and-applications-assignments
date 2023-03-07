# A17 - Giovanni Demasi, 10656704

import numpy as np

if __name__ == '__main__':

    n = 530     # number of students
    z = 120     # think time of the students, seconds

    s1 = 80 / 1000    # moodle server average service time, seconds
    s2 = 120 / 1000   # file server average service time, seconds
    s3 = 11 / 1000    # db server average service time, seconds

    v1 = 1            # moodle server visits
    v2 = 0.75         # file server visits
    v3 = 10           # db server visits

    # demand of each station
    d = np.multiply([v1, v2, v3], [s1, s2, s3])
    print("> Demand of each station")
    for i in range(0, 3):
        print("D" + str(i + 1) + " = " + f'{d[i] :.4f}')

    # Mean Value Analysis (MVA) algorithm
    nk = [0, 0, 0]
    for i in range(1, n+1):
        rk = np.multiply(d, np.add(nk, 1))
        x = np.divide(i, np.add(z, np.sum(rk)))
        nk = np.multiply(x, rk)

    print("> System throughput")
    print("X = " + f'{x :.4f}')

    # utilization of each station
    u = np.multiply(x, d)
    print("> Utilization of each station")
    for i in range(0, 3):
        print("U" + str(i + 1) + " = " + f'{u[i] :.4f}')

    r = np.sum(rk)
    print("> System response time")
    print("R = " + f'{r :.4f}')

    notThink = x * r
    print("> Average number of students not thinking")
    print("N not think = " + f'{notThink :.4f}')

