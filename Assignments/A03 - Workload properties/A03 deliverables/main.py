# A03 - GIOVANNI DEMASI, 10656704

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

if __name__ == '__main__':
    # opening the file to analyze
    file = open("Data1.txt", "r")
    IAi = []
    # reading lines from the file
    for line in file:
        IAi.append(float(line))
    sortedIA = np.sort(IAi)

    mu = np.mean(IAi)  # mean of input samples

    m1 = np.mean(IAi)               # first moment, equal to the mean
    m2 = np.mean(np.power(IAi, 2))  # second moment
    m3 = np.mean(np.power(IAi, 3))  # third moment
    m4 = np.mean(np.power(IAi, 4))  # fourth moment
    m5 = np.mean(np.power(IAi, 5))  # fifth moment

    cm2 = np.mean(np.power(np.subtract(IAi, mu), 2))  # second central moment
    cm3 = np.mean(np.power(np.subtract(IAi, mu), 3))  # third central moment
    cm4 = np.mean(np.power(np.subtract(IAi, mu), 4))  # fourth central moment
    cm5 = np.mean(np.power(np.subtract(IAi, mu), 5))  # fifth central moment

    sm3 = np.mean(np.power(np.divide(np.subtract(IAi, mu), math.sqrt(cm2)), 3))  # third standardized moment
    sm4 = np.mean(np.power(np.divide(np.subtract(IAi, mu), math.sqrt(cm2)), 4))  # fourth standardized moment
    sm5 = np.mean(np.power(np.divide(np.subtract(IAi, mu), math.sqrt(cm2)), 5))  # fifth standardized moment

    sd = np.sqrt(cm2)   # standard deviation
    cv = sd / mu        # coefficient of variation
    kurtosis = sm4 - 3  # excess kurtosis, equal to fourth standardized moment minus 3

    p10 = np.percentile(IAi, 10)  # 10 percentage percentile
    p25 = np.percentile(IAi, 25)  # 25 percentage percentile
    p50 = np.percentile(IAi, 50)  # 50 percentage percentile
    p75 = np.percentile(IAi, 75)  # 75 percentage percentile
    p90 = np.percentile(IAi, 90)  # 90 percentage percentile

    # for completeness, here it is reported an example of percentile computation using the method seen in class
    # h10 = (len(IAi) - 1) * (10 / 100) + 1
    # if h10 == len(IAi):
    #    p10 = sortedIA[len(sortedIA)-1]
    # else:
    #    p10 = sortedIA[math.floor(h10)] + (h10 - math.floor(h10)) * \
    #          (sortedIA[math.floor(h10)+1] - sortedIA[math.floor(h10)])

    cc1 = np.mean(np.multiply(np.subtract(IAi[0:len(IAi) - 1], mu),
                              np.subtract(IAi[0 + 1:len(IAi)], mu)))  # cross covariance lags 1
    cc2 = np.mean(np.multiply(np.subtract(IAi[0:len(IAi) - 2], mu),
                              np.subtract(IAi[0 + 2:len(IAi)], mu)))  # cross covariance lags 2
    cc3 = np.mean(np.multiply(np.subtract(IAi[0:len(IAi) - 3], mu),
                              np.subtract(IAi[0 + 3:len(IAi)], mu)))  # cross covariance lags 3

    pearson1 = cc1 / np.mean(
        np.power(np.subtract(IAi[0:len(IAi) - 1], mu), 2))  # pearson correlation coefficient lags 1
    pearson2 = cc2 / np.mean(
        np.power(np.subtract(IAi[0:len(IAi) - 2], mu), 2))  # pearson correlation coefficient lags 2
    pearson3 = cc3 / np.mean(
        np.power(np.subtract(IAi[0:len(IAi) - 3], mu), 2))  # pearson correlation coefficient lags 3

    # computation of the approximated CDF
    Fx = []
    for i in range(0, len(sortedIA)):
        Fx.append((i + 1) / len(sortedIA))

    print("1st moment = " + f'{m1 :.4f}')
    print("2nd moment = " + f'{m2 :.4f}')
    print("3rd moment = " + f'{m3 :.4f}')
    print("4th moment = " + f'{m4 :.4f}')
    print("5th moment = " + f'{m5 :.4f}')

    print("2nd central moment = " + f'{cm2 :.4f}')
    print("3rd central moment = " + f'{cm3 :.4f}')
    print("4th central moment = " + f'{cm4 :.4f}')
    print("5th central moment = " + f'{cm5 :.4f}')

    print("3rd standardized moment = " + f'{sm3 :.4f}')
    print("4th standardized moment = " + f'{sm4 :.4f}')
    print("5th standardized moment = " + f'{sm5 :.4f}')

    print("Standard deviation = " + f'{sd :.4f}')
    print("Coefficient of variation = " + f'{cv :.4f}')
    print("(Excess) Kurtosis = " + f'{kurtosis :.4f}')

    print("10% percentile = " + f'{p10 :.4f}')
    print("25% percentile = " + f'{p25 :.4f}')
    print("50% percentile = " + f'{p50 :.4f}')
    print("75% percentile = " + f'{p75 :.4f}')
    print("90% percentile = " + f'{p90 :.4f}')

    print("Cross covariance for lags 1 = " + f'{cc1 :.4f}')
    print("Cross covariance for lags 2 = " + f'{cc2 :.4f}')
    print("Cross covariance for lags 3 = " + f'{cc3 :.4f}')

    print("Pearson correlation coefficient for lags 1 = " + f'{pearson1 :.4f}')
    print("Pearson correlation coefficient for lags 2 = " + f'{pearson2 :.4f}')
    print("Pearson correlation coefficient for lags 3 = " + f'{pearson3 :.4f}')

    # approximated CDF (Cumulative Distribution Function) graph
    plt.plot(sortedIA, Fx, color="fuchsia")
    plt.xlabel("Sorted inter-arrivals")
    plt.ylabel(r'$F_x$ (x) = $ \frac{1}{N} \sum_{i=1}^N I(y_i \leq x)$')
    plt.title("Approximated CDF")
    plt.show()
