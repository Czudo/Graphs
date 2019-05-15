import matplotlib.pyplot as plt
import numpy as np
import plot
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


def SIRmodel(u, t, beta, r):
    S, I, R = u
    return np.array([-beta*I*S, beta*I*S-r*I, r*I])


def SIRmodel2(u, t, beta, r):  # reduced SIR model
    S, I = u
    return np.array([-beta*I*S, beta*I*S-r*I])


def R0Formula():
    beta = np.linspace(0.1, 1, 10)
    r = np.linspace(0.1, 1, 10)
    init = [10, 5, 0]
    N = init[0]

    R0 = np.zeros((len(beta), len(r)))

    # i don't know how to check R0 by solving the model numerically :C
    for j in range(len(r)):
        for i in range(len(beta)):
            R0[i][j] = beta[i] * N / r[j]

    xs, ys = np.meshgrid(r, beta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(xs, ys, R0, alpha=0.7, color='blue')

    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel(r'$r$')
    ax.set_zlabel('$R_0$')
    plt.show()
    fig.savefig('SIRModel/R0Formula')


def plotPhasePortrait(S0, I0, beta, r, axes):
    t = np.linspace(0, 15, 1000)
    # colors for plot
    colors = ['magenta', 'cyan', 'greenyellow']

    for j in range(0, len(I0)):
        u = odeint(SIRmodel2, [S0, I0[j]], t, args=(beta, r))
        axes.plot(u[:, 0], u[:, 1], color=colors[j], label=r"$I_0 = $" + str(I0[j]))

    axes.set_xlabel(r"$S$")
    axes.set_ylabel(r"$I$")

    axes = plot.phasePortrait(axes, SIRmodel2, (-0.2, 3.5), (-0.2, 5.5), args=(beta, r))
    axes.legend(loc='upper right')
    return axes


def plotSIRreduced(S0, I0, beta, r, axes):
    t = np.linspace(0, 100, 1000)

    u = odeint(SIRmodel2, [S0, I0], t, args=(beta, r))
    axes.plot(t, u[:, 0], color='blue', label="$S$, $S_0=$" + str(S0))
    axes.plot(t, u[:, 1], color='red', label="$I$, $I_0=$" + str(I0))
    axes.set_title(r"$\beta = $"+str(beta)+", $r = $"+str(r))
    axes.set_xlabel(r"$t$")
    axes.set_ylabel(r"$S/I$")
    axes.legend(loc='upper right')
    axes.set_xlim([0, 20])

    return axes


def plotSIR(S0, I0, R0, beta, r, axes):
    t = np.linspace(0, 100, 1000)

    u = odeint(SIRmodel, [S0, I0, R0], t, args=(beta, r))
    axes.plot(t, u[:, 0], color='blue', label="$S$, $S_0=$" + str(S0))
    axes.plot(t, u[:, 1], color='red', label="$I$, $I_0=$" + str(I0))
    axes.plot(t, u[:, 2], color='grey', label="$R$, $R_0=$" + str(R0))
    axes.set_title(r"$\beta = $"+str(beta)+", $r = $"+str(r))
    axes.set_xlabel(r"$t$")
    axes.set_ylabel(r"$S/I/R$")
    axes.legend(loc='upper right')
    axes.set_xlim([0, 20])

    return axes


def phasePortrait():
    beta = [0.3, 3]
    r = [0.3, 3]
    S0 = 3
    I0 = [0.5, 1.0, 3.0]
    R0 = 0
    fig1, ax1 = plt.subplots(2, 2)
    fig2, ax2 = plt.subplots(2, 2)
    fig3, ax3 = plt.subplots(2, 2)
    for i in range(0, len(beta)):
       for j in range(0, len(r)):
           ax1[i][j] = plotPhasePortrait(S0, I0, beta[i], r[j], ax1[i][j])
           ax1[i][j].title.set_text(r'$\beta = $' + str(beta[i])+', $r = $' + str(r[j]) + ", $S_0 = $" + str(S0))
           ax2[i][j] = plotSIRreduced(S0, I0[0], beta[i], r[j], ax2[i][j])
           ax2[i][j].tick_params('y', reset=True)
           ax3[i][j] = plotSIR(S0, I0[0], R0, beta[i], r[j], ax3[i][j])
           ax3[i][j].tick_params('y', reset=True)
    fig1.tight_layout()
    fig1.savefig('SIRModel/SIRphasePortrait')
    fig2.tight_layout()
    fig2.savefig('SIRModel/SIRrealizationReduced')
    fig3.tight_layout()
    fig3.savefig('SIRModel/SIRrealization')


def totalInfected(N):
    R0 = np.linspace(0, 10, 50)
    all = N
    r = [0.1, 0.2, 0.8]
    t = np.linspace(0, 15, 1000)
    X0 = np.array([N-1, 1, 0])  # all population=N, S0=N-1, I0=1, R0=0

    fig = plt.figure()
    for j in r:
        totalInfected = []
        for i in R0:
            beta = j*i/(N-1)
            u = odeint(SIRmodel, X0, t, args=(beta, j))
            S, I, R = u.T
            totalInfected.append((R[-1]+I[-1])/all)
        plt.plot(R0, totalInfected, '-o', label='$r = $' + str(j))
    plt.axvline(x=1, color='red', label='$R_0 = 1$')
    plt.plot()
    plt.xlabel("$R_0$")
    plt.legend()
    plt.ylabel("total infected")
    fig.savefig("SIRModel/totalInfectedSIR.png")


if __name__ == "__main__":
    R0Formula()
    phasePortrait()
    totalInfected(100)
