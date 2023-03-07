# A02 - GIOVANNI DEMASI, 10656704

import statistics as stat
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

if __name__ == '__main__':
    # opening the file to analyze
    file = open("Log1.csv", "r")

    IAi = []    # inter-arrival times, in seconds

    # reading lines from the file
    for line in file:
        IAi.append(float(line))

    nAi = len(IAi)   # number of inter-arrivals
    nA = nAi + 1     # number of requests, assumed to be equal to the number on inter-arrival times plus one

    A_bar = sum(IAi) / nAi   # average inter-arrival time
    ARate = 1 / A_bar        # arrival rate

    std = stat.stdev(IAi)  # variability - standard deviation of inter-arrival times

    # computation of the arrival times, given the inter arrivals
    Ai = [0]    # assuming that the arrival time of the first request is at time 0
    for i in range(0, nAi):
        Ai.append(Ai[i] + IAi[i])

    Si = 1.2            # service time of each request, in seconds
    Ri = []             # response time of each request, in seconds
    Ci = [Ai[0] + Si]   # completion times, since the system is initially empty the first request is served immediately

    # computation of the completion times
    for i in range(1, nA):
        Ci.append(max(Ai[i], Ci[i - 1]) + Si)

    # computation of the response times
    for i in range(0, nA):
        Ri.append(Ci[i] - Ai[i])

    # average Response Time per request, in seconds
    R = sum(Ri) / len(Ri)

    print("Average inter-arrival time = " + f'{A_bar :.4f}')
    print("Arrival rate = " + f'{ARate :.4f}')
    print("Inter-arrival time variability = " + f'{std :.4f}')
    print("Average response time = " + f'{R :.4f}')

    # correlation diagram, computed using the i-th inter-arrival as x coordinate
    # and the i-th+1 inter-arrivals as y coordinate
    plt.scatter(IAi[0: nAi - 1], IAi[1: nAi], color="orange", s=5)
    plt.xlabel('Inter-arrival time i')
    plt.ylabel('Inter-arrival time i+1')
    plt.title('Inter-arrival times')
    plt.show()
