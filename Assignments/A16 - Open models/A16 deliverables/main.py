# A16 - Giovanni Demasi, 10656704

import numpy as np

if __name__ == '__main__':

    # all jobs arrive according to a poisson process
    l1 = 10           # web server arrival rate, jobs / second
    l2 = l1           # jobs / second
    l3 = 5            # storage server arrival rate, jobs / second

    s1 = 85/1000      # average service time of web server, seconds
    s2 = 75/1000      # average service time of db server, seconds
    s3 = 60/1000      # average service time of storage server, seconds

    # throughput and arrival rate, assuming to have a stable system
    l = l1 + l3
    x = l

    # visits of each station
    print("> Visit of each station")
    v = np.divide([l1, l2, l1+l3], l)
    for i in range(0, 3):
        print("V" + str(i + 1) + " = " + f'{v[i] :.4f}')

    # demand of each station
    print("> Demand of each station")
    d = np.multiply(v, [s1, s2, s3])
    for i in range(0, 3):
        print("D" + str(i + 1) + " = " + f'{d[i] :.4f}')

    # throughput of each station
    xi = [l1, l2, l1+l3]

    # utilization of each station
    print("> Utilization of each station")
    u = np.multiply(xi, [s1, s2, s3])
    for i in range(0, 3):
        print("U" + str(i + 1) + " = " + f'{u[i] :.4f}')

    print("> System throughput")
    print("X = " + f'{x :.4f}')

    #  residence time of each station
    rk = np.divide(d, np.subtract(1, u))

    # average number of jobs in each station
    print("> Average number of jobs in each station")
    n = np.multiply(rk, x)
    for i in range(0, 3):
        print("N" + str(i + 1) + " = " + f'{n[i] :.4f}')

    # average system response time
    print("> System average response time")
    r = np.sum(rk)
    print("R = " + f'{r :.4f}')
