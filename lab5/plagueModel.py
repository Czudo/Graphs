import matplotlib.pyplot as plt
import numpy as np
import plot
from scipy.integrate import odeint


def PModel(u, t, b, beta, k):
    S, I = u
    return np.array([S*b-beta*I*S, beta*I*S-k*I])


def plotPlagueModel(S0, I0, b, beta, k):
    t = np.linspace(0, 10, 1000)
    # declare empty figures
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots(1, 3, sharey='all')
    # colors for plot
    colors = ['magenta', 'cyan', 'greenyellow', 'blue']

    for i in range(0, len(I0)):
        #
        u = odeint(PModel, [S0, I0[i]], t, args=(b, beta, k))

        ax2[i].plot(t, u[:, 0], color='blue', label="$S$")
        ax2[i].plot(t, u[:, 1], color='red', label="$I$")

        ax2[i].set_title(r"$I_0 = $"+str(I0[i]), fontsize=16)
        ax2[i].set_xlabel(r"$t$", fontsize=16)
        ax2[i].set_ylabel(r"$S/I$", fontsize=16)

        ax2[i].legend(loc='upper right', fontsize=12)
        ax2[i].set_xlim([0, 5])
        ax2[i].tick_params('y', reset=True)

        ax1.plot(u[:, 0], u[:, 1], color=colors[i], label="$I_0 =  $"+str(I0[i]))
        ax1.set_xlabel(r"$S$")
        ax1.set_ylabel(r"$I$")
        ax1.set_aspect('equal')

    ax1 = plot.phasePortrait(ax1, PModel, (-0.5, 4), (-0.5, 4), args=(b, beta, k))
    ax1.legend(loc='best', fontsize=12)

    fig1.savefig('plagueModel/phasePortrait')
    fig2.tight_layout()
    fig2.savefig('plagueModel/populationsIS')


if __name__ == "__main__":
    b, beta, k = 3, 3, 3
    # initial conditions
    S0 = 1
    I0 = [0.1, 0.3, 1.3]
    plotPlagueModel(S0, I0, b, beta, k)
