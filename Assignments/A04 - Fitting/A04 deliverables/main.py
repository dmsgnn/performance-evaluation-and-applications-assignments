# A04 - GIOVANNI DEMASI, 10656704

import math
import numpy as np
from scipy.optimize import minimize, fsolve
import sympy as sym
from sympy import symbols
import matplotlib
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', 'The iteration is not making good progress')
matplotlib.use('TkAgg')


# estimation of exponential distribution parameter, using the method of moments
def exponentialMM(mu):
    l = 1 / mu
    return l


# estimation of uniform distribution parameters, using the method of moments
def uniformMM(x1, x2):
    y = x1 - (1 / 2) * math.sqrt(12 * (x2 - math.pow(x1, 2)))
    z = x1 + (1 / 2) * math.sqrt(12 * (x2 - math.pow(x1, 2)))
    return [y, z]


# estimation of the two-stage hyper-Exponential distribution parameters, using the method of moments
def hyperExponentialMM(param, *data):
    x1, x2, x3 = data
    p1, lambda1, lambda2 = param
    return ([((((p1 / lambda1) + ((1 - p1) / lambda2)) / x1) - 1),
             (((2 * ((p1 / lambda1 ** 2) + ((1 - p1) / lambda2 ** 2))) / x2) - 1),
             (((6 * ((p1 / lambda1 ** 3) + ((1 - p1) / lambda2 ** 3))) / x3) - 1)])


# estimation of the two-stage hypo-Exponential distribution parameters, using the method of moments
def hypoExponentialMM(param, *data):
    x1, x2 = data
    lambda1, lambda2 = param
    return ([((1 / (lambda1 - lambda2)) * ((lambda1 / lambda2) - (lambda2 / lambda1)) / x1) - 1,
             ((2 / (lambda1 - lambda2)) * ((lambda1 / lambda2 ** 2) - (lambda2 / lambda1 ** 2)) / x2) - 1])


# estimation of the exponential distribution parameter, using the Maximum Likelihood Estimation
def exponentialMLE(params, data):
    s, N = data
    l = params
    negLL = N * math.log(l) - l * s
    return - negLL


# estimation of the two-stage hyper-Exponential distribution parameters, using the Maximum Likelihood Estimation
def hyperExponentialMLE(params, data):
    trace = data
    p1, l1, l2 = params
    negLL = 0
    for s in trace:
        negLL += math.log(p1 * l1 * math.pow(math.e, -l1 * s) + (1 - p1) * l2 * math.pow(math.e, -l2 * s))
    return - negLL


# estimation of the two-stage hypo-Exponential distribution parameters, using the Maximum Likelihood Estimation
def hypoExponentialMLE(params, data):
    trace = data
    l1, l2 = params
    negLL = 0
    for s in trace:
        negLL += math.log((((l1 * l2) / (l1 - l2)) * ((math.pow(math.e, -l2 * s)) - (math.pow(math.e, -l1 * s)))))
    return - negLL


# METHODS (USED TO DOUBLE-CHECK) REPORTED FOR COMPLETENESS PURPOSES :
# estimation of the two-stage hyper-Exponential distribution parameters, using the method of moments (w/ sympy)
def hyperExponentialMM2(x1, x2, x3):
    p1, lambda1, lambda2 = symbols('x, y, z', real=True)
    return sym.solve([(((p1 / lambda1) + ((1 - p1) / lambda2)) / x1) - 1,
                      ((2 * ((p1 / lambda1 ** 2) + ((1 - p1) / lambda2 ** 2))) / x2) - 1,
                      ((6 * ((p1 / lambda1 ** 3) + ((1 - p1) / lambda2 ** 3))) / x3) - 1], [p1, lambda1, lambda2])


# estimation of the two-stage hypo-Exponential distribution parameters, using the method of moments (w/ sympy)
def hypoExponentialMM2(x1, x2):
    lambda1, lambda2 = symbols('x, y', real=True)
    return sym.solve([((1 / (lambda1 - lambda2)) * ((lambda1 / lambda2) - (lambda2 / lambda1)) / x1) - 1,
                      ((2 / (lambda1 - lambda2)) * ((lambda1 / lambda2 ** 2) - (lambda2 / lambda1 ** 2)) / x2) - 1],
                     [lambda1, lambda2])


# estimation of the two-stage hypo-Exponential distribution parameters, using the method of moments
# with analytical formulas (significant solution only if cv is between 0.5 and 1)
def hypoMM(mu, cvar):
    l1 = (2 / mu) * math.pow(1 + math.sqrt(1 + 2 * ((math.pow(cvar, 2)) - 1)), -1)
    l2 = (2 / mu) * math.pow(1 - math.sqrt(1 + 2 * ((math.pow(cvar, 2)) - 1)), -1)
    return [l1, l2]


if __name__ == '__main__':
    # opening the file to analyze
    file = open("Traces.csv", "r")
    traces = [[], [], []]
    # reading lines from the file
    for line in file:
        traces[0].append(float(line.split(", ")[0]))
        traces[1].append(float(line.split(", ")[1]))
        traces[2].append(float(line.split(", ")[2]))

    # sorting input samples
    sortedTraces = np.sort(traces)

    # computation of the trace approximated CDF
    Fx = []
    for j in range(0, len(sortedTraces[0])):
        Fx.append((j + 1) / len(sortedTraces[0]))

    expMM = []          # exponential parameter of the traces, computed with the MM
    uniMM = []          # uniform parameters of the traces, computed with the MM
    hyperExpMM = []     # hyper-Exponential parameters of the traces, computed with the MM
    hypoExpMM = []      # hypo-Exponential parameters of the traces, computed with the MM
    expMLE = []         # estimation of Exponential parameter of the traces, computed with MLE
    hyperExpMLE = []    # estimation of hyper-Exponential parameters of the traces, computed with MLE
    hypoExpMLE = []     # estimation of hypo-Exponential parameters of the traces, computed with MLE

    for i in range(0, len(traces)):
        # computation of 1st, 2nd and 3rd moment
        m1 = np.mean(traces[i])
        m2 = np.mean(np.power(traces[i], 2))
        m3 = np.mean(np.power(traces[i], 3))

        # coefficient of variation, which can be used to understand when fitting is possible
        cv = np.std(traces[i]) / m1

        # estimation of parameters using method of moments
        expMM.append(exponentialMM(m1))
        uniMM.append(uniformMM(m1, m2))
        hyperExpMM.append(fsolve(hyperExponentialMM, np.array([0.4, 0.8 / m1, 1.2 / m1]), args=(m1, m2, m3)).tolist())
        hypoExpMM.append(fsolve(hypoExponentialMM, np.array([1 / (0.3 * m1), 1 / (0.7 * m1)]), args=(m1, m2)).tolist())

        # estimation of parameters using Maximum Likelihood Estimation
        boundsHyper = ((0, 1), (0, None), (0, None))  # parameter bounds used for the hyper-exp estimation
        expMLE.append(
            minimize(exponentialMLE, np.array(0.1), method='Nelder-Mead',
                     args=[np.sum(traces[i]), len(traces[i])]).x.tolist())
        hyperExpMLE.append(
            minimize(hyperExponentialMLE, np.array([0.4, 0.8 / m1, 1.2 / m1]), method='Nelder-Mead', args=traces[i],
                     bounds=boundsHyper).x.tolist())
        hypoExpMLE.append(minimize(hypoExponentialMLE, np.array([1 / (0.3 * m1), 1 / (0.7 * m1)]), method='Nelder-Mead',
                                   args=traces[i]).x.tolist())

        # Uniform distribution
        uniCDF = [[], [], []]
        a = uniMM[i][0]
        b = uniMM[i][1]
        x = np.linspace(sortedTraces[i][0], sortedTraces[i][len(sortedTraces[i]) - 1], 1000)
        uniX = np.linspace(a, b, 1000)
        for j in uniX:
            if j < a:
                uniCDF[i].append(0)
            elif a <= j <= b:
                uniCDF[i].append((j - a) / (b - a))
            elif j > b:
                uniCDF[i].append(1)

        # Exponential distribution
        expCDF = [[], [], []]
        expCDF_MLE = [[], [], []]
        lambdaMM = expMM[i]
        lambdaMLE = expMLE[i][0]
        for j in x:
            expCDF[i].append(1 - math.pow(math.e, -lambdaMM * j))
            expCDF_MLE[i].append(1 - math.pow(math.e, -lambdaMLE * j))

        # Hyper-Exponential distribution
        hyperExpCDF = [[], [], []]
        hyperExpCDF_MLE = [[], [], []]
        p1MM = hyperExpMM[i][0]
        lambda1MM = hyperExpMM[i][1]
        lambda2MM = hyperExpMM[i][2]
        p1MLE = hyperExpMLE[i][0]
        lambda1MLE = hyperExpMLE[i][1]
        lambda2MLE = hyperExpMLE[i][2]
        for j in x:
            hyperExpCDF[i].append(
                1 - (p1MM * math.pow(math.e, -lambda1MM * j)) - (1 - p1MM) * (math.pow(math.e, - lambda2MM * j)))
            hyperExpCDF_MLE[i].append(
                1 - (p1MLE * math.pow(math.e, -lambda1MLE * j)) - (1 - p1MLE) * (math.pow(math.e, - lambda2MLE * j)))

        # Hypo-Exponential distribution
        hypoExpCDF = [[], [], []]
        hypoExpCDF_MLE = [[], [], []]
        l1MM = hypoExpMM[i][0]
        l2MM = hypoExpMM[i][1]
        l1MLE = hypoExpMLE[i][0]
        l2MLE = hypoExpMLE[i][1]
        for j in x:
            hypoExpCDF[i].append(1 - ((l2MM * math.pow(math.e, - l1MM * j)) / (l2MM - l1MM)) + (
                    (l1MM * math.pow(math.e, - l2MM * j)) / (l2MM - l1MM)))
            hypoExpCDF_MLE[i].append(1 - ((l2MLE * math.pow(math.e, - l1MLE * j)) / (l2MLE - l1MLE)) + (
                    (l1MLE * math.pow(math.e, - l2MLE * j)) / (l2MLE - l1MLE)))

        # printing of the results
        print(">>> " + str(i + 1))
        print("m1 = " + f'{m1 :.4f}')
        print("m2 = " + f'{m2 :.4f}')
        print("m3 = " + f'{m3 :.4f}')
        print("cv = " + f'{cv :.4f}')
        print(">> MM ESTIMATION")
        print("> UNIFORM")
        print("a = " + f'{a :.4f}')
        print("b = " + f'{b :.4f}')
        print("> EXPONENTIAL")
        print("l = " + f'{lambdaMM :.4f}')
        print("> HYPER EXPONENTIAL")
        print("p1 = " + f'{p1MM :.4f}')
        print("l1 = " + f'{lambda1MM :.4f}')
        print("l2 = " + f'{lambda2MM :.4f}')
        print("> HYPO EXPONENTIAL")
        print("l1 = " + f'{l1MM :.4f}')
        print("l2 = " + f'{l2MM :.4f}')
        print(">> MLE ESTIMATION")
        print("> EXPONENTIAL")
        print("l = " + f'{lambdaMLE :.4f}')
        print("> HYPER EXPONENTIAL")
        print("p1 = " + f'{p1MLE :.4f}')
        print("l1 = " + f'{lambda1MLE :.4f}')
        print("l2 = " + f'{lambda2MLE :.4f}')
        print("> HYPO EXPONENTIAL")
        print("l1 = " + f'{l1MLE :.4f}')
        print("l2 = " + f'{l2MLE :.4f}')

        # MM CDF (Cumulative Distribution Function)
        plt.plot(sortedTraces[i], Fx, label="Trace", color="blue")
        plt.plot(uniX, uniCDF[i], label="Uniform", color="purple")
        plt.plot(x, expCDF[i], label="Exponential", color="green")
        plt.plot(x, hyperExpCDF[i], label="Hyper-Exp", color="red")
        plt.plot(x, hypoExpCDF[i], label="Hypo-Exp", color="orange")
        plt.xlabel("Time")
        plt.ylabel("CDF")
        plt.title("Method of Moments")
        plt.legend(loc='best')
        plt.show()

        plt.clf()

        # MLE CDF (Cumulative Distribution Function)
        fig = plt.plot(sortedTraces[i], Fx, label="Trace", color="blue")
        plt.plot(x, expCDF_MLE[i], label="Exponential", color="green")
        plt.plot(x, hyperExpCDF_MLE[i], label="Hyper-Exp", color="red")
        plt.plot(x, hypoExpCDF_MLE[i], label="Hypo-Exp", color="orange")
        plt.xlabel("Time")
        plt.ylabel("CDF")
        plt.title("Maximum Likelihood")
        plt.legend(loc='best')
        plt.show()
