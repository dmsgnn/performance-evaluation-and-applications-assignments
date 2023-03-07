# A19 - Giovanni Demasi, 10656704

import numpy as np

if __name__ == '__main__':

    # Arrival rates, Poisson process
    le = 5      # requests / second
    lp = 10     # requests / second

    # Resource 1 -> CRM
    # Resource 2 -> FS
    # Two type of users: employees and providers

    # Demand at each server, for employees and providers
    d1e = 50/1000   # seconds
    d2e = 100/1000  # seconds
    d1p = 60/1000   # seconds
    d2p = 40/1000   # seconds

    # Arrival rate and demand matrices
    l = [[le, le],
         [lp, lp]]
    D = [[d1e, d2e],
         [d1p, d2p]]

    # Utilization
    Uck = np.multiply(D, l)
    Uk = sum(Uck)

    # Visits, equal to 1 since requests need always to be handled by both servers
    v = [[1, 1],
         [1, 1]]

    # Throughput
    Xc = [le, lp]
    Xck = np.multiply(v, l)
    Xk = sum(Xck)
    X = sum(Xc)

    # Residence time
    Rck = np.divide(D, np.subtract(1, Uk))
    Phick = np.divide(Rck, v)

    # Queue length
    Nck = np.multiply(Xck, Phick)
    Nk = sum(Nck)
    Nc = sum(Nck.transpose())
    N = sum(Nc)

    Phik = sum(np.multiply(np.divide(Xck, [Xk, Xk]), Phick))

    # Response time
    Rk = np.divide(Nk, X)
    Rc = sum(Rck.transpose())
    R = sum(Rk)

    print("> Utilization")
    print("  U(CRM) = " + f'{Uk[0] :.4f}')
    print("  U(FS) = " + f'{Uk[1] :.4f}')

    print("> Residence time")
    print("  R(CRM) = " + f'{Rk[0] :.4f}')
    print("  R(FS) = " + f'{Rk[1] :.4f}')

    print("> Response time")
    print("  R = " + f'{R :.4f}')
