import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


def SIRmodel(u,t):
    S = u[0]
    I = u[1]
    R = u[2]
    return np.array([-beta*I*S,beta*I*S-gamma*I,gamma*I])

gamma = 1.0
I0 = 1.0
S0 = 100.0
init = [S0, I0, 0.0]
bvals = [0.01, 0.02, 0.03]
t = np.linspace(0, 100, 1000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i in range(len(bvals)):
    beta = bvals[i]
    u = odeint(SIRmodel, init, t)
    axes[i].plot(t, u[:,0], label="$S$")
    axes[i].plot(t, u[:,1], label="$I$")
    axes[i].plot(t, u[:,2], label="$R$")
    axes[i].set_title(r"$\beta = $"+str(beta),fontsize=16)
    axes[i].set_xlabel(r"$t$",fontsize=16)
    axes[i].set_ylabel(r"$S/I/R$",fontsize=16)
    axes[i].legend(loc=5,fontsize=12)
    axes[i].set_xlim([0,20])
plt.tight_layout()
plt.show()