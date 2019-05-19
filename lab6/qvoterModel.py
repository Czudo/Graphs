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
    :param p: float, a probability of contagion
    :return: list of tuples: (name of graph, graph, probability p)
    """
    return [#('er', nx.gnm_random_graph(N, 3*N)),
            ('ws1', nx.watts_strogatz_graph(N, 4, 0.01)),
            ('ws2', nx.watts_strogatz_graph(N, 4, 0.02)),
            ('ba', nx.barabasi_albert_graph(N, 4))]


def qvoterModel(G):
    P = 100  # no independent
    N = 1000  # no MC
    n = 100  # no spinsons
    q = 3
    opinions = {i: int(2*(round(random.random())-0.5)) for i in range(n)}
    nx.set_node_attributes(G, opinions, 'spin')

    print(G.nodes(data=True))
    for k in range(P):
        for j in range(N):
            for i in range(n):
                spinson = chooseSpinson()
                spinsonAction(spinson)


if __name__ == '__main__':
    G = getRandomGraphs(100)
    G = G[0][1]
    qvoterModel(G)
