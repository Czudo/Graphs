import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import numpy as np
import multiprocessing


def chooseSpinson():
    return 1


def spinsonAction(i):
    return 1


def getRandomGraphs(N):
    """
    Function creates random graphs: 2D lattice - '2d', Erdos-Renyi - 'er', Watts–Strogatz - 'ws',
                                    Barabassi-Albert - 'ba'

    :param N: integer, number of nodes
    :return: list of tuples: (name of graph, graph)
    """
    return [#('er', nx.gnm_random_graph(N, 3*N)),
            ('ws1', nx.watts_strogatz_graph(N, 4, 0.01)),
            ('ws2', nx.watts_strogatz_graph(N, 4, 0.02)),
            ('ba', nx.barabasi_albert_graph(N, 4))]


def qvoterModel(G):
    P = 100  # number of independent nums
    N = 1000  # number of MC steps
    n = 100  # number of spinsons
    q = 3
    epsilon =0.01
    possibleSpins = [True, False]
    opinions = {i: random.choice(possibleSpins) for i in range(n)}
    nx.set_node_attributes(G, opinions, 'spin')

    spinsons = list(G.nodes())

    for i in range(n):
        spinson = random.choice(spinsons)
        if random.random() <= P/n:
            neighbors = list(G.neighbors(spinson))
            listOfSpins = [0] * q
            for j in range(q):
                neighbor = random.choice(neighbors)
                listOfSpins[j] = G.node[neighbor]['spin']
            if len(set(listOfSpins)) == 1:  # if spins of chosen neighbors are the same
                G.node[spinson]['spin'] = listOfSpins[0]
            else:
                if random.random() <= epsilon:
                    G.node[spinson]['spin'] = not G.node[spinson]['spin']


if __name__ == '__main__':
    G = getRandomGraphs(100)
    G = G[0][1]
    qvoterModel(G)
