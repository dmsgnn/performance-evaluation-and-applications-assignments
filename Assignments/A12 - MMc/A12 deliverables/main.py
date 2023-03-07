# A12 - Giovanni Demasi, 10656704

from math import *

if __name__ == '__main__':
    # single server
    l = 50          # arrival rate, jobs/seconds
    d = 15 / 1000   # average service time, seconds
    m = 1 / d       # service rate, 1/seconds

    print("> M/M/1")

    # probability of having one job in the system
    n1 = (1 - (l / m)) * pow((l / m), 1)
    print("P(N = 1) = " + f'{n1 :.4f}')

    # probability of having less than four job in the system
    rho = l * d
    n4p = pow(rho, 4 + 1)
    n4 = (1 - (l / m)) * pow((l / m), 4)
    n4l = 1 - n4p - n4
    print("P(N < 4) = " + f'{n4l :.4f}')

    # Utilization of the system, equal to the probability of having more than 0 jobs in the system
    u = pow(rho, 0 + 1)
    print("U = " + f'{u :.4f}')

    # average number of jobs in the queue
    nq = pow(rho, 2) / (1 - rho)
    print("Nq" + " = " + f'{nq :.4f}')

    # average response time
    r = d / (1 - rho)
    print("R = " + f'{r :.4f}')

    # response time greater than 0,5 seconds
    t = 0.5  # seconds
    r5 = exp(-t / r)
    print("P(R > 0.5s) = " + f'{r5 :.4f}')

    # 90 percentile of response time distribution
    p90 = - log((1 - (90 / 100))) * r
    print("\u03b8(90) = " + f'{p90 :.4f}')

    # Multiple server (2)
    ns = 2      # number of servers
    l = 85      # arrival rate, jobs/seconds

    rho = (l * d) / ns

    print("\n")
    print("> M/M/2")

    # average and total utilization of the system
    ut = l / m
    ua = l / (2 * m)
    print("U = " + f'{ut :.4f}')
    print("U\u0304 = " + f'{ua :.4f}')

    # probability of having exactly one job in the system
    n1 = 2 * (1 - rho) / (1 + rho) * pow(rho, 1)
    print("P(N = 1) = " + f'{n1 :.4f}')

    # probability of having less than 4 jobs in the system
    n0 = (1 - rho) / (1 + rho)
    n2 = 2 * (1 - rho) / (1 + rho) * pow(rho, 2)
    n3 = 2 * (1 - rho) / (1 + rho) * pow(rho, 3)
    n4l = n0 + n1 + n2 + n3
    print("P(N < 4) = " + f'{n4l :.4f}')

    # average queue length (job not in service)
    th = (pow(rho, 2) * d) / (1 - pow(rho, 2))
    nq = l * th
    print("Nq = " + f'{nq :.4f}')

    # average response time
    r = d / (1 - pow(rho, 2))
    print("R = " + f'{r :.4f}')
