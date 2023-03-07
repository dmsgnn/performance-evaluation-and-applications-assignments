# PROJECT D - GIOVANNI DEMASI, 10656704

import math
import numpy as np
from scipy.optimize import fsolve
import matplotlib
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', 'The iteration is not making good progress')
matplotlib.use('TkAgg')


# Functions related to Method of Moments estimation
# Exponential distribution parameter
def exponentialMM(mu):
    l = 1 / mu
    return l


# Uniform distribution parameters
def uniformMM(x1, x2):
    y = x1 - (1 / 2) * math.sqrt(12 * (x2 - math.pow(x1, 2)))
    z = x1 + (1 / 2) * math.sqrt(12 * (x2 - math.pow(x1, 2)))
    return [y, z]


# Two-stage hyper-Exponential distribution parameters
def hyperExponentialMM(param, *data):
    x1, x2, x3 = data
    p1, lambda1, lambda2 = param
    return ([((((p1 / lambda1) + ((1 - p1) / lambda2)) / x1) - 1),
             (((2 * ((p1 / lambda1 ** 2) + ((1 - p1) / lambda2 ** 2))) / x2) - 1),
             (((6 * ((p1 / lambda1 ** 3) + ((1 - p1) / lambda2 ** 3))) / x3) - 1)])


# Two-stage hypo-Exponential distribution parameters
def hypoExponentialMM(param, *data):
    x1, x2 = data
    lambda1, lambda2 = param
    return ([((1 / (lambda1 - lambda2)) * ((lambda1 / lambda2) - (lambda2 / lambda1)) / x1) - 1,
             ((2 / (lambda1 - lambda2)) * ((lambda1 / lambda2 ** 2) - (lambda2 / lambda1 ** 2)) / x2) - 1])


if __name__ == '__main__':
    # the four traces files are opened
    traceA = open("Traces/TraceD-A.txt", "r")
    traceB = open("Traces/TraceD-B.txt", "r")
    traceC = open("Traces/TraceD-C.txt", "r")
    traceD = open("Traces/TraceD-D.txt", "r")

    # bi-dimensional array to contain all the different trace
    traces = [[], [], [], []]

    # reading lines from each trace, saving them in the corresponding array
    # arrival times are transformed from milliseconds to seconds for coherence with other parameters
    for line in traceA:
        traces[0].append(float(line)/1000)
    for line in traceB:
        traces[1].append(float(line)/1000)
    for line in traceC:
        traces[2].append(float(line)/1000)
    for line in traceD:
        traces[3].append(float(line)/1000)

    # bi-dimensional array to contain the different inter-arrival times
    inter_arrivals = [[], [], [], []]

    # amount of arrival times
    num_lines = len(traces[0])

    # for each pair of arrival times, one inter-arrival is computed
    # it is assumed that at time 0 there is not an arrival, so the amount of
    # inter-arrivals will be equal to the amount of arrival times, minus 1
    for analytical_l in range(1, num_lines):
        inter_arrivals[0].append(traces[0][analytical_l] - traces[0][analytical_l - 1])
        inter_arrivals[1].append(traces[1][analytical_l] - traces[1][analytical_l - 1])
        inter_arrivals[2].append(traces[2][analytical_l] - traces[2][analytical_l - 1])
        inter_arrivals[3].append(traces[3][analytical_l] - traces[3][analytical_l - 1])

    # amount of inter-arrival times
    num_lines = len(inter_arrivals[0])

    # sorting inter-arrival times of each trace
    sortedInterArrivals = [np.sort(inter_arrivals[0]),
                           np.sort(inter_arrivals[1]),
                           np.sort(inter_arrivals[2]),
                           np.sort(inter_arrivals[3])]

    # computation of the trace approximated CDF
    Fx = []
    for j in range(0, num_lines):
        Fx.append((j + 1) / num_lines)

    expMM = []          # exponential parameter of the traces
    uniMM = []          # uniform parameters of the traces
    hyperExpMM = []     # hyper-Exponential parameters of the traces
    hypoExpMM = []      # hypo-Exponential parameters of the traces

    uniCDF = [[], [], [], []]       # CDF of the uniform fitted distribution
    expCDF = [[], [], [], []]       # CDF of the exponential fitted distribution
    hyperExpCDF = [[], [], [], []]  # CDF of the hyper-exponential fitted distribution
    hypoExpCDF = [[], [], [], []]   # CDF of the hypo-exponential fitted distribution

    for i in range(0, len(inter_arrivals)):
        # computation of 1st, 2nd and 3rd moment
        m1 = np.mean(inter_arrivals[i])
        m2 = np.mean(np.power(inter_arrivals[i], 2))
        m3 = np.mean(np.power(inter_arrivals[i], 3))

        # coefficient of variation, which can be used to understand when fitting is possible
        cv = np.std(traces[i]) / m1

        # estimation of parameters using method of moments
        expMM.append(exponentialMM(m1))
        uniMM.append(uniformMM(m1, m2))
        hyperExpMM.append(fsolve(hyperExponentialMM, np.array([0.4, 0.8 / m1, 1.2 / m1]), args=(m1, m2, m3)).tolist())
        hypoExpMM.append(fsolve(hypoExponentialMM, np.array([1 / (0.3 * m1), 1 / (0.7 * m1)]), args=(m1, m2)).tolist())

        # Uniform distribution
        a = uniMM[i][0]
        b = uniMM[i][1]
        x = np.linspace(sortedInterArrivals[i][0], sortedInterArrivals[i][len(sortedInterArrivals[i]) - 1], 1000)
        uniX = np.linspace(a, b, 1000)
        for j in uniX:
            if j < a:
                uniCDF[i].append(0)
            elif a <= j <= b:
                uniCDF[i].append((j - a) / (b - a))
            elif j > b:
                uniCDF[i].append(1)

        # Exponential distribution
        lambdaMM = expMM[i]
        for j in x:
            expCDF[i].append(1 - math.pow(math.e, -lambdaMM * j))

        # Hyper-Exponential distribution
        p1MM = hyperExpMM[i][0]
        lambda1MM = hyperExpMM[i][1]
        lambda2MM = hyperExpMM[i][2]

        for j in x:
            hyperExpCDF[i].append(
                1 - (p1MM * math.pow(math.e, -lambda1MM * j)) - (1 - p1MM) * (math.pow(math.e, - lambda2MM * j)))

        # Hypo-Exponential distribution
        l1MM = hypoExpMM[i][0]
        l2MM = hypoExpMM[i][1]
        for j in x:
            hypoExpCDF[i].append(1 - ((l2MM * math.pow(math.e, - l1MM * j)) / (l2MM - l1MM)) + (
                    (l1MM * math.pow(math.e, - l2MM * j)) / (l2MM - l1MM)))

        # computation of the analytical exponential distribution using the
        # lambda parameter found with method of moments, as double check to verify that
        # exponential distribution well represents the dataset distribution
        analytical_exp = []
        analytical_l = lambdaMM
        x_check = np.linspace(min(sortedInterArrivals[i]), max(sortedInterArrivals[i]), num_lines)
        for t in x_check:
            analytical_exp.append(1 - math.pow(math.e, -analytical_l * t))

        # printing of the results
        print("> Trace " + str(i + 1))
        print("cv = " + f'{cv :.4f}')
        print("EXPONENTIAL")
        print("l = " + f'{lambdaMM :.4f}')

        # method of moments CDF (Cumulative Distribution Function)
        # all the distributions are plotted, even if only one is used
        plt.scatter(sortedInterArrivals[i], Fx, label="Trace", color="c", s=24, marker='+')
        plt.plot(uniX, uniCDF[i], label="Uniform", color="m")
        plt.plot(x, expCDF[i], label="Exponential", color="g")
        plt.plot(x, hyperExpCDF[i], label="Hyper-Exp", color="orange")
        plt.plot(x, hypoExpCDF[i], label="Hypo-Exp", color="b")
        plt.title("Trace " + str(i+1) + " - Method of Moments")
        plt.legend(loc='best')
        plt.show()
        plt.clf()

        # this plot aims to show that the analytical exponential distribution
        # well represents the dataset distribution
        plt.scatter(sortedInterArrivals[i], Fx, label="Dataset", color="c", s=24, marker='+')
        plt.plot(x_check, analytical_exp, label="Analytical", color="orange")
        plt.title("Trace " + str(i+1) + " - Exponential")
        plt.legend(loc='best')
        plt.show()
