import matplotlib.pyplot as plt
import numpy as np
import plot
from scipy.integrate import odeint

a = 4
b = 3
beta = 3
k = 3

def PModel(u,t):
    S, I = u
    return np.array([S*b-beta*I*S, beta*I*S-k*I])



S0 = 1
I0 = [0.1, 0.3, 1.3]
t = np.linspace(0,10,1000)
fig1, ax1 = plt.subplots(1, 1)
fig2, ax2 = plt.subplots(1, 3)  # przerwy między subplotami
for i in range(0,len(I0)):
    u = odeint(PModel, [S0, I0[i]], t)
    ax2[i].plot(t, u[:, 0], label="$S$")
    ax2[i].plot(t, u[:, 1], label="$I$")

    ax2[i].set_title(r"$I_0 = $"+str(I0[i]), fontsize=16)
    ax2[i].set_xlabel(r"$t$", fontsize=16)
    ax2[i].set_ylabel(r"$S/I$", fontsize=16)
    ax2[i].legend(loc=5, fontsize=12)
    ax2[i].set_xlim([0, 2.5])


    ax1.plot(u[:, 0], u[:, 1], label="$I_0 =  $"+str(I0[i]))
    ax1.set_xlabel('S')
    ax1.set_ylabel('I')
    ax1.set_aspect('equal')


ax1 = plot.phasePortrait(ax1, PModel, (-0.5, a), (-0.5, a))
ax1.legend(fontsize=12)


plt.show()




# fig, axes = plt.subplots(1, 3,figsize=(15,4))
# for i in range(len(I0)):
#     beta = bvals[i]
#     u = odeint(rhs,init,t)
#     axes[i].plot(t,u[:,0],label="$S$")
#     axes[i].plot(t,u[:,1],label="$I$")
#     axes[i].plot(t,u[:,2],label="$R$")
#     axes[i].set_title(r"$\beta = $"+str(beta),fontsize=16)
#     axes[i].set_xlabel(r"$t$",fontsize=16)
#     axes[i].set_ylabel(r"$S/I/R$",fontsize=16)
#     axes[i].legend(loc=5,fontsize=12)
#     axes[i].set_xlim([0,20])
#
# plt.tight_layout()
# plt.show()