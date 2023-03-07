# A13 - Giovanni Demasi, 10656704

from math import *

if __name__ == '__main__':
    # Single server
    k = 16
    l = 1200            # packets / second
    d = 1.25 / 1000     # seconds
    m = 1 / d

    print("> M/M/1/16")

    rho = l / m

    # utilization
    u = (rho - pow(rho, k + 1)) / (1 - pow(rho, k + 1))
    print("U = " + f'{u :.4f}')

    # probability of having 14 packets in the system
    p14 = ((1 - rho) / (1 - pow(rho, k + 1))) * pow(rho, 14)
    print("P(N = 14) = " + f'{p14 :.4f}')

    # average number of packets in the system
    n = rho / (1 - rho) - ((k + 1) * pow(rho, k + 1)) / (1 - pow(rho, k + 1))
    print("N = " + f'{n :.4f}')

    # Throughput of the system
    x = l * ((1 - pow(rho, k)) / (1 - pow(rho, k + 1)))
    print("X = " + f'{x :.4f}')

    # drop rate of the system
    dr = l * ((pow(rho, k) - pow(rho, k + 1)) / (1 - pow(rho, k + 1)))
    print("Dr = " + f'{dr :.4f}')

    # average response time
    r = d * ((1 - (k + 1) * pow(rho, k) + k * pow(rho, k + 1)) / ((1 - rho) * (1 - pow(rho, k))))
    print("R = " + f'{r :.4f}')

    # average time spent in the queue, theta
    theta = r - d
    print("\u03b8 = " + f'{theta :.4f}')

    # Multiple servers
    c = 2

    print("\n")
    print("> M/M/2/16")

    rho = l / (c * m)
    p0 = pow((pow(c * rho, c) / factorial(c)) * ((1 - pow(rho, k - c + 1)) / (1 - rho)) + (
                pow(c * rho, 0) / factorial(0)) + (pow(c * rho, 1) / factorial(1)), -1)

    # utilization
    ub = 0
    for n in range(1, c + 1):
        ub += n * (p0 / factorial(n)) * pow(l / m, n)
    for n in range(c + 1, k + 1):
        ub += c * (p0 / (factorial(c) * pow(c, n - c))) * pow(l / m, n)
    ub /= c
    print("U\u0304 = " + f'{ub :.4f}')

    # probability of having 14 packets in the system
    p14 = (p0 / (factorial(c) * pow(c, 14-c))) * pow(l/m, 14)
    print("P(N = 14) = " + f'{p14 :.4f}')

    # average number of packets in the system
    n = 0
    for i in range(1, k+1):
        if i < c:
            n += i * (p0/factorial(i)) * pow(l/m, i)
        else:
            n += i * (p0/(factorial(c) * pow(c, i-c))) * pow(l/m, i)
    print("N = " + f'{n :.4f}')

    # Throughput of the system
    x = l * (1 - p0/(factorial(c) * pow(c, k-c)) * pow(l/m, k))
    print("X = " + f'{x :.4f}')

    # drop rate of the system
    dr = l * p0/(factorial(c) * pow(c, k-c)) * pow(l/m, k)
    print("Dr = " + f'{dr :.4f}')

    # average response time
    r = n / x
    print("R = " + f'{r :.4f}')

    # average time spent in the queue, theta
    theta = r - d
    print("\u03b8 = " + f'{theta :.4f}')



