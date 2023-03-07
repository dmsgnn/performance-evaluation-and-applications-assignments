# A15 - Giovanni Demasi, 10656704

import numpy as np

if __name__ == '__main__':

    l = 10  # arrival rate, jobs / second

    # service times
    s1 = 40 / 1000   # seconds
    s2 = 100 / 1000  # seconds
    s3 = 120 / 1000  # seconds

    # routing probabilities from state 1
    p10 = 0.5
    p12 = 0.3
    p13 = 0.2
    # routing probabilities from state 2
    p21 = 1
    # routing probabilities from state 3
    p31 = 0.2
    p32 = 0.8

    # throughput is equal to the sum of the arrivals
    x = l

    # system of linear equations in order to find arrival rate of each station
    # l1 = l + p21 * l2 + p31 * l3  ->  -l = -l1 + p21 * l2 + p31 * l3  ->  [-1, p21, p31]
    # l2 = p12 * l1 + p32 * l3      ->   0 = p12 * l1 - l2 + p32 * l3   ->  [p12, -1, p32]
    # l3 = p13 * l1                 ->   0 = p13 * l1 - l3              ->  [p13, 0, -1]

    # Matrices of linear equations
    A = np.array([[-1, p21, p31], [p12, -1, p32], [p13, 0, -1]])
    # Array of known terms
    b = np.array([-l, 0, 0])
    # Solution of the system of linear equation
    li = np.linalg.solve(A, b)

    # visit of each station
    print("> Visit of each station")
    v = np.divide(li, l)
    for i in range(0, 3):
        print("V" + str(i + 1) + " = " + f'{v[i] :.4f}')

    # demand of each station
    print("> Demand of each station")
    d = np.multiply(v, [s1, s2, s3])
    for i in range(0, 3):
        print("D" + str(i + 1) + " = " + f'{d[i] :.4f}')

    # throughput of each station
    print("> Throughput of each station")
    xi = np.multiply(v, x)  # throughput of each station
    for i in range(0, 3):
        print("X" + str(i + 1) + " = " + f'{xi[i] :.4f}')
