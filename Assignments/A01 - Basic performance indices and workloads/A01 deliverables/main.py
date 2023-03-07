# A01 - GIOVANNI DEMASI, 10656704

import numpy as np
import datetime

if __name__ == '__main__':
    # open the log file to analyze
    file = open("apache1.log", "r")
    Ai = []  # time of each request arrival, in millisecond, starting from zero
    Ci = []  # time of each request completion, in millisecond
    Si = []  # service time of each request, in millisecond
    # the time unit used for intermediate computations is milliseconds, this in order to avoid float rounding errors

    # reading all the lines of the log file, acquiring the arrival times
    for line in file:
        string_ts = line.split()[3]
        ts = datetime.datetime.strptime(string_ts, '[%d/%b/%Y:%H:%M:%S.%f')
        Ai.append(ts)
        Si.append(int(line.split()[13]))

    # making arrival times starting from zero
    begin = Ai[0]
    for i in range(0, len(Ai)):
        Ai[i] = int((Ai[i] - begin).total_seconds() * 1000)

    # computation of completion of each request
    Ci.append(Ai[0] + Si[0])
    for i in range(1, len(Ai)):
        Ci.append(max(Ai[i], Ci[i - 1]) + Si[i])

    nA = len(Ai)    # number of total arrivals
    nC = nA         # number of total completions

    B = np.sum(Si)  # busy time
    S = B / nC      # average service time

    T = Ci[len(Ci) - 1]  # total observation time

    U = B / T  # utilization

    aRate = nA / T  # arrival rate
    X = nC / T      # throughput

    Ri = []     # response time of each request
    for i in range(0, len(Ai)):
        Ri.append(Ci[i] - Ai[i])

    W = sum(Ri)     # area of the difference between arrivals and completions

    R = W / nC  # average response time
    N = X * R   # average number of requests in the system

    A_bar = 1 / aRate  # average inter-arrival time

    R1 = sum(i < 1000 for i in Ri) / len(Ri)    # probability of having a response time less than 1 second
    R5 = sum(i < 5000 for i in Ri) / len(Ri)    # probability of having a response time less than 5 seconds
    R10 = sum(i < 10000 for i in Ri) / len(Ri)  # probability of having a response time less than 10 seconds

    # computation of the bi-dimensional array, with sorted arrivals and completions
    AC_history = np.concatenate((Ai, Ci))
    half1 = [1 for i in range(len(Ai))]
    half2 = [-1 for i in range(len(Ci))]
    full = np.concatenate((half1, half2))
    trace = np.vstack((AC_history, full))
    trace = trace[:, trace[0].argsort()]

    Ni = [trace[1][0]]  # amount of requests in the system for each arrival/completion
    for i in range(1, len(trace[1])):
        Ni.append(Ni[i - 1] + trace[1][i])

    N0 = 0  # probability of having 0 jobs in the system
    N1 = 0  # probability of having 1 jobs in the system
    N2 = 0  # probability of having 2 jobs in the system
    N3 = 0  # probability of having 3 jobs in the system

    # computation of the total time in which 0,1,2,3 jobs were present in the system
    for i in range(0, len(Ni) - 1):
        if Ni[i] == 0:
            N0 += trace[0][i + 1] - trace[0][i]
        if Ni[i] == 1:
            N1 += trace[0][i + 1] - trace[0][i]
        if Ni[i] == 2:
            N2 += trace[0][i + 1] - trace[0][i]
        if Ni[i] == 3:
            N3 += trace[0][i + 1] - trace[0][i]

    N0 /= T
    N1 /= T
    N2 /= T
    N3 /= T

    print("Arrival rate = " + f'{(aRate * 1000):.4f}')
    print("Throughput = " + f'{(X * 1000):.4f}')
    print("Average inter-arrival time = " + f'{(A_bar / 1000):.4f}')
    print("Busy time = " + f'{(B / 1000):.4f}')
    print("Utilization = " + f'{U :.4f}')
    print("W = " + f'{(W / 1000):.4f}')
    print("Average service time = " + f'{(S / 1000):.4f}')
    print("Average number of jobs = " + f'{N :.4f}')
    print("Average response time = " + f'{(R / 1000):.4f}')
    print("Probability of having a response time less than 1s = " + f'{R1 :.4f}')
    print("Probability of having a response time less than 5s = " + f'{R5:.4f}')
    print("Probability of having a response time less than 10s = " + f'{R10:.4f}')
    print("Probability of having 0 jobs in the web server = " + f'{N0 :.4f}')
    print("Probability of having 1 jobs in the web server = " + f'{N1 :.4f}')
    print("Probability of having 2 jobs in the web server = " + f'{N2 :.4f}')
    print("Probability of having 3 jobs in the web server = " + f'{N3 :.4f}')
