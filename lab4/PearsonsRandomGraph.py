import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import collections
import numpy as np
import subprocess


def getCoordinates(G):
    coordinates = collections.OrderedDict(sorted(nx.get_node_attributes(G, 'coordinates').items())).values()
    coordinates = list(zip(*coordinates))
    return coordinates


def PearsonsRandomWalk(G, N):
    start = 0
    G.add_node(start, coordinates=[0, 0])
    x, y = 0, 0

    for next in range(1, N+1):
        phi = random.random()*2*math.pi
        x = x + math.cos(phi)
        y = y + math.sin(phi)
        G.add_node(next, coordinates=[x, y])
        G.add_edge(start, next, angle=phi)
        start = next

    [x, y] = getCoordinates(G)
    plt.plot(x, y, '-o', linewidth=0.2, markersize=0.5)
    return max(x), min(x), max(y), min(y)  # return maximal and minimal coordinates to set x and y limits


def distribution(G, N, n):
    An = []
    Bn = []
    for i in range(n):
        x, y = getCoordinates(G[i])
        An.append(sum(1 for k in x if k > 0))
        Bn.append(sum(1 for k in range(len(x)) if x[k] > 0 and y[k] > 0))

    plt.figure()
    results, edges = np.histogram(np.asarray(An)/N, density=True)
    binWidth = edges[1] - edges[0]
    plt.bar(edges[:-1], results*binWidth, binWidth, label='empirical')
    plt.plot([1/2, 1/2] , [0, max(results*binWidth)], 'r', label='theoretical mean')
    plt.legend()
    plt.xlabel(r'$A_n$')
    plt.ylabel('PDF')
    plt.savefig('pearsonsrandomwalk/prw_An_' + str(n) + 'graphs_' + str(N) + 'steps.png')

    plt.figure()
    results, edges = np.histogram(np.asarray(Bn)/N, density=True)
    binWidth = edges[1] - edges[0]
    plt.bar(edges[:-1], results * binWidth, binWidth, label='empirical')
    plt.plot([1 / 4, 1 / 4], [0, max(results * binWidth)], 'r', label='theoretical mean')
    plt.legend()
    plt.xlabel(r'$B_n$')
    plt.ylabel('PDF')
    plt.savefig('pearsonsrandomwalk/pwr_Bn_' + str(n) + 'graphs_' + str(N) + 'steps.png')


def plotOneGraph(G, N):
    [x, y] = getCoordinates(G)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    plt.xlim([min(x) - 0.5, max(x) + 0.5])
    plt.ylim([min(y) - 0.5, max(y) + 0.5])
    plt.xlabel('x')
    plt.ylabel('y')
    ax1.plot(x[0], y[0], '-o', color='blue', linewidth=0.2, markersize=0.5)

    fig1.savefig('pearsonsrandomwalk/prw_' + str(N) + '_{0:04}.png'.format(0))
    for i in range(N):
        ax1.plot([x[i], x[i+1]], [y[i], y[i+1]], '-o', color='blue', linewidth=0.2, markersize=0.5)
        fig1.savefig('pearsonsrandomwalk/prw_' + str(N) + '_{0:04}.png'.format(i+1))

    cmd = ['magick', 'convert', '-delay', '20', '-loop', '0', 'pearsonsrandomwalk/prw_'
           + str(N) + '_*.png', 'pearsonsrandomwalk/gif_prw_' + str(N) + 'steps.gif']
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    G = []  # list of graphs
    n = 10  # number of graphs
    N = 500  # number of steps
    maxX, minX, maxY, minY = 0, 0, 0, 0
    for i in range(n):
        G.append(nx.Graph())
        x1, x2, y1, y2 = PearsonsRandomWalk(G[i], N)
        maxX = max(maxX, x1)
        minX = min(minX, x2)
        maxY = max(maxY, y1)
        minY = min(minY, y2)

    plt.plot([minX, maxX], [0, 0], ':', linewidth=1, color='black')
    plt.plot([0, 0], [minY, maxY], ':', linewidth=1, color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('pearsonsrandomwalk/prw_graphs_' + str(n) + '_' + str(N) + 'steps.png')
    distribution(G, N, n)
    plotOneGraph(G[0], N)
