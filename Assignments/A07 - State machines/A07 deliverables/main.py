# A07 - Giovanni Demasi (10656704)

import numpy as np
import math

if __name__ == '__main__':
    s = 1
    T = 0
    T_max = 100000

    trace = [[T, s]]
    Ts1 = 0
    Ts2 = 0
    Ts3 = 0
    Ts4 = 0
    sensing = 0

    while T < T_max:
        if s == 1:   # state 1 -> temperature sensor
            ns = 2
            l = 0.1  # seconds^(-1)
            dt = - (math.log(np.random.uniform(low=0, high=1)) + math.log(np.random.uniform(low=0, high=1)) + math.log(
                np.random.uniform(low=0, high=1))) / l
            Ts1 += dt
            sensing += 1
        elif s == 2:    # state 2 -> CPU
            a = 10  # seconds
            b = 20  # seconds
            dt = np.random.uniform(low=a, high=b)
            Ts2 += dt
            rand = np.random.uniform(low=0, high=1)
            if rand < 0.5:  # return sensing
                ns = 1
            elif rand < 0.8:  # air
                ns = 3
            else:  # heat
                ns = 4
        elif s == 3:    # state 3 -> air conditioning
            ns = 1
            l = 0.05    # seconds^(-1)
            dt = - math.log(np.random.uniform(low=0, high=1)) / l
            Ts3 += dt
        else:    # state 4 -> heat pump
            ns = 1
            l = 0.03    # seconds^(-1)
            dt = - math.log(np.random.uniform(low=0, high=1)) / l
            Ts4 += dt
        s = ns
        T += dt
        trace.append([T, s])

    Ps1 = Ts1 / T
    Ps2 = Ts2 / T
    Ps4 = Ts3 / T
    Ps5 = Ts4 / T
    X = sensing / T

    print("P(SENS) = " + f'{Ps1 :.4f}')
    print("P(CPU) = " + f'{Ps2 :.4f}')
    print("P(AIR) = " + f'{Ps4 :.4f}')
    print("P(HEAT) = " + f'{Ps5 :.4f}')
    print("X = " + f'{X :.4f}')  # sensing/second
