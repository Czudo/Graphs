import matplotlib.pyplot as plt
import networkx as nx
import random
import math


def initPRandomWalk(n):
    G = nx.Graph()
    start = 0
    G.add_node(start, cords=[0, 0])
    x, y = 0, 0
    plt.figure()
    for i in range(1, n+1):
        phi = random.random()*2*math.pi
        x = x + math.cos(phi)
        y = y + math.sin(phi)
        G.add_node(i, cords=[x, y])
        G.add_edge(start, i, angle=phi)
        start = i

        plt.plot()
    #sort by key
    cords = list(nx.get_node_attributes(G, 'cords').values())

    cords = list(zip(*cords))
    plt.plot(cords[0],cords[1], 'o')


    plt.show()


if __name__ == '__main__':
    initPRandomWalk(10000)