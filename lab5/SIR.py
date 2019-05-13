import matplotlib.pyplot as plt
import numpy as np
import plot
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


def SIRmodel(u, t, beta, r):
    S, I, R = u
    return np.array([-beta*I*S, beta*I*S-r*I, r*I])

def SIRmodel2(u, t, beta, r):
    S, I = u
    return np.array([-beta*I*S, beta*I*S-r*I])


def R0Formula(init):
    beta = np.linspace(0.1, 2, 10)
    r = np.linspace(0.1, 2, 10)
    N = init[0]
    R_0 = np.zeros((len(beta), len(r)))
    #t = np.linspace(0, 10, 1000)
    R_0_teo = np.zeros((len(beta), len(r)))
    for j in range(len(r)):
        for i in range(len(beta)):
            R_0[i][j] = beta[i] * N / r[j]
            u = SIRmodel(init, None, beta[i], r[j])
            print(u)
            R_0_teo[i][j] = np.mean(u[1]/u[2])

    xs, ys = np.meshgrid(r, beta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(xs, ys, R_0, alpha=0.7)
    ax.plot_surface(xs, ys, R_0_teo, alpha=0.7)
    ax.set_xlabel(r'$\beta$')
    ax.set_ylabel(r'$r$')
    ax.set_zlabel('$R_0$')


    plt.show()


def plotSIR2(S0, I0, beta, r, axes):
    t = np.linspace(0, 100, 1000)

    # colors for plot
    colors = ['magenta', 'cyan', 'greenyellow']

    for j in range(0, len(I0)):
        for i in range(0, len(S0)):
            u = odeint(SIRmodel2, [S0[i], I0[j]], t, args=(beta, r))
            axes.plot(u[:, 0], u[:, 1], label=r"$S_0 =  $ " + str(S0[i]) + ", $I_0 = $" + str(I0[j]))

    axes.set_xlabel(r"$S$")
    axes.set_ylabel(r"$I$")


    axes = plot.phasePortrait(axes, SIRmodel2, (-0.5, 7), (-0.5, 7), args=(beta, r))
    axes.legend(loc='best', fontsize=12)
    #axes.title(r"$\beta = $" + str(beta) + ", $r = $" + str(r))
    return axes


def plotSIR(init, bvals, r, axes):
    t = np.linspace(0, 100, 1000)

    for i in range(len(bvals)): # same beta
        beta = bvals[i]
        u = odeint(SIRmodel, init, t, args=(beta, r))
        axes[i].plot(t, u[:, 0], label="$S$")
        axes[i].plot(t, u[:, 1], label="$I$")
        axes[i].plot(t, u[:, 2], label="$R$")
        axes[i].set_title(r"$\beta = $"+str(beta), fontsize=16)
        axes[i].set_xlabel(r"$t$", fontsize=16)
        axes[i].set_ylabel(r"$S/I/R$", fontsize=16)
        axes[i].legend(loc=5, fontsize=12)
        axes[i].set_xlim([0, 20])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    init = [10.0, 5.0, 0.0]
    R0Formula(init)
    #plotSIR(init, bvals, r)
    beta=[0.1, 5]
    r=[0.2, 5]
    # fig = plt.figure()

    # id=221
    # for i in range(0, len(beta)):
    #    for j in range(0, len(r)):
    #        ax = fig.add_subplot(id)
    #        ax = plotSIR2([5.0], [0.5, 1.0, 3.0], beta[i], r[j], ax)
    #        id = id+1
    #plt.show()
