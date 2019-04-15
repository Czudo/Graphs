import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import math


def randomWalk(G, n, start):

    notActual = (255/255, 153/255, 230/255)
    actual = (179/255, 0/255, 134/255)
    nx.set_node_attributes(G, math.inf, 'value')
    nx.set_node_attributes(G, notActual, 'color')

    pos = nx.spring_layout(G)

    G.node[start]['value'] = 0
    G.node[start]['color'] = actual
    saveActualPlot(G, 0, pos)

    for i in range(1, n+1):
        posibleVertices = tuple(G.neighbors(start))
        next = random.choice(posibleVertices)
        if G.node[next]['value'] == math.inf:
            G.node[next]['value'] = i
        G.node[start]['color'] = notActual
        G.node[next]['color'] = actual
        start = next
        saveActualPlot(G, i, pos)

    cmd = ['magick', 'convert', '-delay', '40', '-loop', '0', 'randomwalk2/rw2_*.png', 'randomwalk2/gif_rw2.gif']
    subprocess.call(cmd, shell=True)


def saveActualPlot(G, step, pos):
    fig1 = plt.figure()
    nx.draw(G, pos, labels=dict(G.nodes(data='value')), with_labels=True,
            node_color=tuple(nx.get_node_attributes(G, 'color').values()))
    coordinates = tuple(zip(*tuple(pos.values())))
    plt.xlim([min(coordinates[0])-0.2, max(coordinates[0])+0.2])
    plt.ylim([min(coordinates[1])-0.2, max(coordinates[1])+0.2])
    plt.xlabel('x')
    plt.ylabel('y')
    fig1.savefig('randomwalk2/rw2_{0:04}.png'.format(step))
    plt.close()


if __name__ == '__main__':
    N = [100, 20]  # number of steps ??????
    n = 25  # number of edges ????????

    G = nx.gnm_random_graph(N[1], n)

    print(G.degree())  # get name with 0 degree
    list = []
    for i in G.degree():
        if i[1] == 0:
            list.append(i[0])
    print(list)

    randomWalk(G, 100, 0)

