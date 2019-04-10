import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import collections
import numpy as np

def getCords(G):
    cords = collections.OrderedDict(sorted(nx.get_node_attributes(G, 'cords').items())).values()
    cords = list(zip(*cords))
    return cords


def PearsonsRandomWalk(n, G):
    start = 0
    G.add_node(start, cords=[0, 0])
    x, y = 0, 0

    for i in range(1, n+1):
        phi = random.random()*2*math.pi
        x = x + math.cos(phi)
        y = y + math.sin(phi)
        G.add_node(i, cords=[x, y])
        G.add_edge(start, i, angle=phi)
        start = i

    cords = getCords(G)
    plt.plot(cords[0], cords[1], '-o', linewidth=0.5, markersize=1)
    return max(cords[0]), min(cords[0]), max(cords[1]), min(cords[1])


def distribution(G, N):
    An = [0]*len(G)
    print(An)
    Bn = [0]*len(G)
    for i in range(len(G)):
        x,y = getCords(G[i])
        An[i] = sum(1 for k in x if k > 0)
        Bn[i] = sum(1 for k in range(len(x)) if x[k] > 0 and y[k] > 0)
    plt.figure()
    [unique, counts] = np.unique(np.sort(An), return_counts=True)
    plt.plot(unique, counts)
    plt.savefig('An_{}.png'.format(N))
    print(Bn)
    plt.figure()
    plt.hist(Bn, density=True, bins=10, label='empirical')
    plt.savefig('Bn_{}.png'.format(N))


if __name__ == '__main__':
    G = []
    n = 2000
    N = 1000
    maxx, minx, maxy, miny = 0, 0, 0, 0
    for i in range(0, n):
        G.append(nx.Graph())
        tempmaxx, tempminx, tempmaxy, tempminy = PearsonsRandomWalk(N, G[i])
        maxx = max(maxx, tempmaxx)
        minx = min(minx, tempminx)
        maxy = max(maxy, tempmaxy)
        miny = min(miny, tempminy)

    plt.plot([minx, maxx], [0, 0], ':', linewidth=1, color='black')
    plt.plot([0, 0], [miny, maxy], ':', linewidth=1, color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('PRandomWalk_{}_{}.png'.format(N, n))
    distribution(G, N)
