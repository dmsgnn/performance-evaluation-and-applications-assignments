# A10 - Giovanni Demasi, 10656704

from scipy.integrate import solve_ivp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# parameters of the problem, in Watt
idleP = 0.1
cpuP = 2
ioP = 0.5
gpuP = 10

# duration of tasks, in seconds
idle = 10
cpu = 50
gpuAvg = 20
gpu = 2
ioAvg = 10
io = 5

# parameters used to create the infinitesimal generator matrix
l1 = 1 / idle
l2 = 1 / ioAvg
l3 = 1 / gpuAvg
m1 = 1 / cpu
m2 = 1 / io
m3 = 1 / gpu

# Infinitesimal generator matrix
Q = np.array([[-l1, l1, 0, 0],
              [m1, -m1 - l2 - l3, l3, l2],
              [0, m3, -m3, 0],
              [0, m2, 0, -m2]])


def equations(t, y):
    return Q.transpose() @ y


if __name__ == '__main__':
    p = np.array([1, 0, 0, 0])  # S1 initial state

    s1 = solve_ivp(equations, [0, 500], p.transpose(), t_eval=np.linspace(0, 500, 3050))

    print("> Infinitesimal generator matrix")
    print("   S1	   S2	   S3	   S4")
    print('\n'.join(
        ['\t'.join([bool(cell >= 0) * " " + f'{cell :.4f}' for cell in row]) + "  S" + str(num + 1) for num, row in
         enumerate(Q)]))

    # Computation of the steady state probabilities
    Qp = np.array([[1, l1, 0, 0],
                   [1, -m1 - l2 - l3, l3, l2],
                   [1, m3, -m3, 0],
                   [1, m2, 0, -m2]])

    u = np.array([1, 0, 0, 0])
    pi = np.dot(u, np.linalg.inv(Qp))

    # Steady state solution states probability
    print("> Steady state probabilities")
    print("P(S1) = " + f'{pi[0] :.4f}')
    print("P(S2) = " + f'{pi[1] :.4f}')
    print("P(S3) = " + f'{pi[2] :.4f}')
    print("P(S4) = " + f'{pi[3] :.4f}')

    # State rewards vectors
    alphaP = np.array([0.1, 2, 10, 0.5])  # Power
    alphaU = np.array([0, 1, 1, 1])  # Utilization
    # Transition reward matrices
    xiX = np.array([[0, 0, 0, 0],  # Throughput
                    [1, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])
    xiXgpu = np.array([[0, 0, 0, 0],  # GPU Throughput
                       [0, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0]])
    xiXio = np.array([[0, 0, 0, 0],  # I/O Frequency
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 1, 0, 0]])

    # Steady state computation of performance metrics
    steadyU = np.dot(pi, alphaU.transpose())  # Utilization
    steadyP = np.dot(pi, alphaP.transpose())  # Power
    steadyX = np.sum(np.dot(pi, np.multiply(Q, xiX)))  # Throughput
    steadyXgpu = np.sum(np.dot(pi, np.multiply(Q, xiXgpu)))  # GPU Throughput
    steadyXio = np.sum(np.dot(pi, np.multiply(Q, xiXio)))  # I/O Frequency

    print("> Steady state performance metrics")
    print("U = " + f'{steadyU :.4f}')
    print("P = " + f'{steadyP :.4f}')
    print("X = " + f'{steadyX :.4f}')
    print("X(GPU) = " + f'{steadyXgpu :.4f}')
    print("F(I/O) = " + f'{steadyXio :.4f}')

    # arrays containing the evolution of performance metrics in function of time
    timeU = []
    timeP = []
    timeX = []
    timeXgpu = []
    timeXio = []

    # Computation of performance metrics in function of time
    for i in range(0, len(s1.t)):
        timeU.append(np.dot(np.array([s1.y[0][i], s1.y[1][i], s1.y[2][i], s1.y[3][i]]), alphaU.transpose()))
        timeP.append(np.dot(np.array([s1.y[0][i], s1.y[1][i], s1.y[2][i], s1.y[3][i]]), alphaP.transpose()))
        timeX.append(np.sum(np.dot(np.array([s1.y[0][i], s1.y[1][i], s1.y[2][i], s1.y[3][i]]), np.multiply(Q, xiX))))
        timeXgpu.append(
            np.sum(np.dot(np.array([s1.y[0][i], s1.y[1][i], s1.y[2][i], s1.y[3][i]]), np.multiply(Q, xiXgpu))))
        timeXio.append(
            np.sum(np.dot(np.array([s1.y[0][i], s1.y[1][i], s1.y[2][i], s1.y[3][i]]), np.multiply(Q, xiXio))))

    # plot with the states probability in function of time
    plt.plot(s1.t, s1.y[0], label="$S_1$", color="blue")
    plt.plot(s1.t, s1.y[1], label="$S_2$", color="red")
    plt.plot(s1.t, s1.y[2], label="$S_3$", color="orange")
    plt.plot(s1.t, s1.y[3], label="$S_4$", color="purple")
    plt.xlabel("Time [seconds]")
    plt.ylabel("$P(S_i)$")
    plt.title("State Probability")
    plt.legend(loc='best')
    plt.show()

    # plot of all the performance metrics together, in function of time
    plt.plot(s1.t, timeU, label="U", color="blue")
    plt.plot(s1.t, timeP, label="P", color="red")
    plt.plot(s1.t, timeX, label="X", color="orange")
    plt.plot(s1.t, timeXgpu, label="$X_{GPU}$", color="purple")
    plt.plot(s1.t, timeXio, label="$X_{I/O}$", color="green")
    plt.xlabel("Time [seconds]")
    plt.ylabel(" ")
    plt.title("Performance metrics")
    plt.legend(loc='best')
    plt.show()

    # plot of the Utilization in function of time
    plt.plot(s1.t, timeU, label="U", color="blue")
    plt.xlabel("Time [seconds]")
    plt.ylabel(r'$E[\alpha_k(t)] = \sum_{i=1} \pi_i(t) \cdot \alpha_{ki}$')
    plt.title("Utilization")
    plt.legend(loc='best')
    plt.show()

    # plot of the Power in function of time
    plt.plot(s1.t, timeP, label="P", color="red")
    plt.xlabel("Time [seconds]")
    plt.ylabel(r'$E[\alpha_k(t)] = \sum_{i=1} \pi_i(t) \cdot \alpha_{ki}$')
    plt.title("Power")
    plt.legend(loc='best')
    plt.show()

    # plot of the Throughput in function of time
    plt.plot(s1.t, timeX, label="X", color="orange")
    plt.xlabel("Time [seconds]")
    plt.ylabel(r'$E[\xi_k(t)] = \sum_{i=1} \pi_i(t) \sum_{j \ne i} q_{ij} \cdot \xi_{k, ij}$')
    plt.title("System Throughput")
    plt.legend(loc='best')
    plt.show()

    # plot of the GPU Throughput in function of time
    plt.plot(s1.t, timeXgpu, label="$X_{GPU}$", color="purple")
    plt.xlabel("Time [seconds]")
    plt.ylabel(r'$E[\xi_k(t)] = \sum_{i=1} \pi_i(t) \sum_{j \ne i} q_{ij} \cdot \xi_{k, ij}$')
    plt.title("GPU Throughput")
    plt.legend(loc='best')
    plt.show()

    # plot of the I/O Frequency in function of time
    plt.plot(s1.t, timeXio, label="$X_{I/O}$", color="green")
    plt.xlabel("Time [seconds]")
    plt.ylabel(r'$E[\xi_k(t)] = \sum_{i=1} \pi_i(t) \sum_{j \ne i} q_{ij} \cdot \xi_{k, ij}$')
    plt.title("I/O Frequency")
    plt.legend(loc='best')
    plt.show()
