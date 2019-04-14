import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
from matplotlib import patches
import math

def randomWalk(N, n, j, start):
    G = nx.gnm_random_graph(N, n)
    nx.draw(G)
    plt.show()

    nx.set_node_attributes(G, math.inf, 'value')
    nx.set_node_attributes(G, False, 'actual')

    # for i in G.nodes():
    #    G.node[i]['value'] = i
    #    print(G.node[i]['value'])
    # save starting position
    G.node[start]['value'] = 0
    G.node[start]['actual'] = True
    for i in range(1, j):
        posibleVertices = list(G.neighbors(start))
        next = random.choice(posibleVertices)
        if G.node[next]['value'] == math.inf:
            G.node[next]['value'] = i
        G.node[start]['actual'] = False
        G.node[next]['actual'] = True
        start = next
        # save actual position (plot)

    for i in G.nodes():
        print(G.node[i]['value'])


if __name__ == '__main__':
    N = [100, 20]  # number of steps
    n = 20  # number of edges
    randomWalk(n, N[1], 100, 0)
