# A05 - Giovanni Demasi, 10656704

import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

if __name__ == '__main__':
    # opening the file to analyze
    file = open("random.csv", "r")
    rand_nums = [[], [], []]
    # reading lines from the file
    for line in file:
        rand_nums[0].append(float(line.split(", ")[0]))
        rand_nums[1].append(float(line.split(", ")[1]))
        rand_nums[2].append(float(line.split(", ")[2]))

    # length of samples to be generated
    size = 500

    # Fx for approximated CDF
    Fx = []
    for i in range(0, size):
        Fx.append((i + 1) / size)

    # Uniform
    uni = []
    uniF = []
    a = 5
    b = 15
    for i in rand_nums[1]:  # 2nd column
        uniF.append(a + i * (b - a))

    x = np.linspace(min(uniF), max(uniF), 1000)
    for t in x:
        if t < a:
            uni.append(0)
        elif a <= t <= b:
            uni.append((t - a) / (b - a))
        elif t > b:
            uni.append(1)

    print("> Uniform")
    for n in uniF[0:10]:
        print(f'{n :.4f}')
    plt.plot(np.sort(uniF), Fx, label="Approximated", color="orange")
    plt.plot(x, uni, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Uniform")
    plt.legend(loc='best')
    plt.show()

    # Discrete
    disc = []
    discF = []
    values = [5, 10, 15]
    probs = [0.3, 0.4, 0.3]
    csum = np.cumsum(probs, dtype=float)
    for i in range(0, 500):
        rand = rand_nums[0][i]
        for x in range(0, len(csum)):
            if rand < csum[x]:
                discF.append(values[x])
                break

    x = np.linspace(min(discF)-2, max(discF)+2, 1000)
    for t in x:
        done = False
        for v in range(0, len(values)):
            if t < values[v]:
                if v == 0:
                    disc.append(0)
                else:
                    disc.append(csum[v - 1])
                done = True
                break
        if not done:
            disc.append(1)

    print("> Discrete")
    for n in discF[0:10]:
        print(n)
    plt.plot(np.sort(discF), Fx, label="Approximated", color="orange")
    plt.plot(x, disc, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Discrete")
    plt.legend(loc='best')
    plt.show()

    # Exponential
    exp = []
    expF = []
    l = 1 / 10
    for i in rand_nums[1]:  # 2nd column
        expF.append(- math.log(i) / l)

    x = np.linspace(min(expF), max(expF), 1000)
    for t in x:
        exp.append(1 - math.pow(math.e, -l * t))

    print("> Exponential")
    for n in expF[0:10]:
        print(f'{n :.4f}')
    plt.plot(np.sort(expF), Fx, label="Approximated", color="orange")
    plt.plot(x, exp, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Exponential")
    plt.legend(loc='best')
    plt.show()

    # Hyper-Exponential
    hyper_exp = []
    hyperExpF = []
    p1 = 0.3
    l1 = 0.05
    l2 = 0.175
    for i in range(0, len(rand_nums[0])):
        if rand_nums[0][i] < p1:
            hyperExpF.append(- math.log(rand_nums[1][i]) / l1)
        else:
            hyperExpF.append(- math.log(rand_nums[1][i]) / l2)

    x = np.linspace(min(hyperExpF), max(hyperExpF), 1000)
    for t in x:
        hyper_exp.append(1 - (p1 * math.pow(math.e, - l1 * t)) - (1 - p1) * (math.pow(math.e, - l2 * t)))

    print("> Hyper-Exponential")
    for n in hyperExpF[0:10]:
        print(f'{n :.4f}')
    plt.plot(np.sort(hyperExpF), Fx, label="Approximated", color="orange")
    plt.plot(x, hyper_exp, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Hyper Exponential")
    plt.legend(loc='best')
    plt.show()

    # Hypo-Exponential
    hypo_exp = []
    hypoExpF = []
    l1 = 0.25
    l2 = 0.16667
    for i in range(0, len(rand_nums[1])):
        hypoExpF.append(- (math.log(rand_nums[1][i]) / l1) - (math.log(rand_nums[2][i]) / l2))

    x = np.linspace(min(hypoExpF), max(hypoExpF), 1000)
    for t in x:
        hypo_exp.append(
            1 - ((l2 * math.pow(math.e, - l1 * t)) / (l2 - l1)) + ((l1 * math.pow(math.e, - l2 * t)) / (l2 - l1)))

    print("> Hypo-Exponential")
    for n in hypoExpF[0:10]:
        print(f'{n :.4f}')
    plt.plot(np.sort(hypoExpF), Fx, label="Approximated", color="orange")
    plt.plot(x, hypo_exp, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Hypo Exponential")
    plt.legend(loc='best')
    plt.show()

    # Hyper-Erlang
    hyper_erl = []
    hyperErlF = []
    k = [1, 2]
    lambdas = [0.05, 0.35]
    p = [0.3, 0.7]
    erl1 = []
    erl2 = []
    for i in range(0, len(rand_nums[0])):
        erl1.append(- math.log(rand_nums[1][i]) / lambdas[0])
        erl2.append(- (math.log(rand_nums[1][i]) + math.log(rand_nums[2][i])) / lambdas[1])
    for i in range(0, len(rand_nums[0])):
        if rand_nums[0][i] < p[0]:
            hyperErlF.append(erl1[i])
        else:
            hyperErlF.append(erl2[i])

    x = np.linspace(min(hyperErlF), max(hyperErlF), 1000)
    for t in x:
        hyper_erl.append(1 - p[0] * math.exp(-lambdas[0] * t) - (p[1]) * (
                math.exp(-lambdas[1] * t) + math.exp(-lambdas[1] * t) * lambdas[1] * t))

    print("> Hyper-Erlang")
    for n in hyperErlF[0:10]:
        print(f'{n :.4f}')
    plt.plot(np.sort(hyperErlF), Fx, label="Approximated", color="orange")
    plt.plot(x, hyper_erl, label="Analytical", color="blue")
    plt.xlabel("Time")
    plt.ylabel("CDF")
    plt.title("Hyper Erlang")
    plt.legend(loc='best')
    plt.xlim(0, 50)
    plt.show()
