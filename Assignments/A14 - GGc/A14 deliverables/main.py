# A14 - Giovanni Demasi, 10656704

from math import *

if __name__ == '__main__':
    # Single core server
    l = 500  # jobs / second, Poisson process
    # Hypo Exponential parameters
    mu1 = 1500  # jobs / second
    mu2 = 1000  # jobs / second

    print("> M/G/1")

    d = 1 / mu1 + 1 / mu2   # average of the hypo exponential
    m2 = 2 * (1/pow(mu1, 2) + 1/(mu1 * mu2) + 1/(pow(mu2, 2)))  # second moment of the hypo exponential
    rho = l * d

    # Utilization of the system
    u = l * d
    print("U = " + f'{u :.4f}')

    # (exact) Average response time
    r = d + (l * m2) / (2 * (1 - rho))
    print("R = " + f'{r :.4f}')

    # (exact) Average number of jobs in the system
    n = l * r
    print("N = " + f'{n :.4f}')

    # Dual-core server
    l = 4000  # jobs / second, 4 stage Erlang distribution
    k = 4

    print("\n")
    print("> G/G/2")

    t = k / l  # average of the erlang distribution, average of inter-arrival
    d = 1 / mu1 + 1 / mu2  # average of the hypo exponential, average service
    ca = 1 / sqrt(k)  # arrival coefficient of variation
    cv = sqrt(pow(mu1, 2) + pow(mu2, 2)) / (mu1 + mu2)  # service coefficient of variation
    l = 1 / t

    rho = d / (2 * t)

    # Utilization of the system
    u = (l * d) / 2
    print("U\u0304 = " + f'{u :.4f}')

    # Approximate average response time
    r = d + ((pow(ca, 2) + pow(cv, 2)) / 2) * (pow(rho, 2) * d) / (1 - pow(rho, 2))
    print("R = " + f'{r :.4f}')

    # Approximate average number of jobs in the system
    n = l * r
    print("N = " + f'{n :.4f}')

