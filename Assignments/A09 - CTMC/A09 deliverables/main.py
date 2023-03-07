# A09 - Giovanni Demasi, 10656704

from scipy.integrate import solve_ivp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# parameters of the problem
cellUp = 20
cellDown = 2
wifiUp = 3
wifiDown = 8
reset = 100

# parameters used to generate the matrix
l1 = 1 / cellUp
l2 = 1 / wifiUp
l3 = 1 / reset
m1 = 1 / cellDown
m2 = 1 / wifiDown

# Infinitesimal generator matrix
Q = np.array([[-l1 - l2 - l3, l1, l2, l3],
              [m1, -m1 - l2, 0, l2],
              [m2, 0, -m2 - l1, l1],
              [0, m2, m1, -m2 - m1]])

# S1 4G and Wi-Fi active
# S2 4G down, Wi-Fi active
# S3 Wi-Fi down, 4G active
# S4 4G and Wi-Fi down


def equations(t, y):
    return Q.transpose() @ y


if __name__ == '__main__':
    p = np.array([1, 0, 0, 0])  # S1 initial state

    s1 = solve_ivp(equations, [0, 300], p.transpose(), t_eval=np.linspace(0, 300, 1830))
    s2 = solve_ivp(equations, [0, 10], p.transpose(), t_eval=np.linspace(0, 10, 61))

    state = ['1', '2', '3', '4']
    print("> Infinitesimal generator matrix")
    print("   S1	   S2	   S3	   S4")
    print('\n'.join(['\t'.join([bool(cell >= 0) * " " + f'{cell :.4f}' for cell in row]) + "  S" + str(num+1) for num, row in enumerate(Q)]))

    # States probability plot in [0, 300] hours range
    plt.plot(s1.t, s1.y[0], label="$S_1$", color="blue")
    plt.plot(s1.t, s1.y[1], label="$S_2$", color="red")
    plt.plot(s1.t, s1.y[2], label="$S_3$", color="orange")
    plt.plot(s1.t, s1.y[3], label="$S_4$", color="purple")
    plt.xlabel("Time [hours]")
    plt.ylabel("$P (S_i)$")
    plt.title("State Probability")
    plt.legend(loc='best')
    plt.show()

    # States probability plot in [0, 10] hours range
    plt.plot(s2.t, s2.y[0], label="$S_1$", color="blue")
    plt.plot(s2.t, s2.y[1], label="$S_2$", color="red")
    plt.plot(s2.t, s2.y[2], label="$S_3$", color="orange")
    plt.plot(s2.t, s2.y[3], label="$S_4$", color="purple")
    plt.xlabel("Time [hours]")
    plt.ylabel("$P (S_i)$")
    plt.title("State Probability")
    plt.legend(loc='best')
    plt.show()
