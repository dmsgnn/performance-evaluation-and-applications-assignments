# A08 - Giovanni Demasi, 10656704

import numpy as np
import math

if __name__ == '__main__':
    s = 1
    t = 0
    Tmax = 100000

    trace = [t, s]
    Ts1 = 0
    Ts2 = 0
    Ts3 = 0
    start = 0

    while t < Tmax:
        if s == 1:
            ns = 2
            l = 0.05  # seconds^ -1
            dt = - math.log(np.random.uniform(low=0, high=1)) / l
            Ts1 += dt
            start += 1
        elif s == 2:
            lFS = 1         # seconds^ -1
            lStartGC = 0.1  # seconds^ -1
            dtFS = - math.log(np.random.uniform(low=0, high=1)) / lFS
            dtStartGC = - math.log(np.random.uniform(low=0, high=1)) / lStartGC
            dt = min(dtFS, dtStartGC)
            if dt == dtFS:
                ns = 1
                Ts2 += dt
            else:
                ns = 3
        else:
            lMidGC = 0.4    # seconds^ -1
            lFullGC = 0.3   # seconds^ -1
            dtFull = - math.log(np.random.uniform(low=0, high=1)) / lFullGC
            dtMid = - math.log(np.random.uniform(low=0, high=1)) / lMidGC
            dt = min(dtFull, dtMid)
            if dt == dtMid:
                ns = 2
            else:
                ns = 1
            Ts3 += dt
        s = ns
        t += dt
        trace.append([t, s])

    Ps1 = Ts1 / t
    Ps2 = Ts2 / t
    Ps3 = Ts3 / t
    X = start / t

    print("P(PREP) = " + f'{Ps1 :.4f}')
    print("P(FS) = " + f'{Ps2 :.4f}')
    print("P(GC) = " + f'{Ps3 :.4f}')
    print("X = " + f'{X :.4f}')
