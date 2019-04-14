import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import math


def randomWalk(N, n, j, start, G=None):

    if start == 0:  # if its first try
        G = nx.gnm_random_graph(N, n)
    if not list(G.neighbors(start)):  # if vertex has no friends
        randomWalk(N, n, j, start+1, G)  # try with next vertex
        return  # dont do the same for start what has done with next
    noActual = (255/255, 153/255, 230/255)
    actual = (179/255, 0/255, 134/255)
    nx.set_node_attributes(G, math.inf, 'value')
    nx.set_node_attributes(G, noActual, 'color')

    pos = nx.spring_layout(G)

    G.node[start]['value'] = 0
    G.node[start]['color'] = actual
    saveActualPlot(G, 0, pos)

    for i in range(1, j+1):
        posibleVertices = list(G.neighbors(start))
        next = random.choice(posibleVertices)
        if G.node[next]['value'] == math.inf:
            G.node[next]['value'] = i
        G.node[start]['color'] = noActual
        G.node[next]['color'] = actual
        start = next
        saveActualPlot(G, i, pos)
    cmd = ['magick', 'convert', '-delay', '40', '-loop', '0', 'randomwalk2/rw2_*.png', 'randomwalk2/gif_rw2.gif']
    subprocess.call(cmd, shell=True)


def saveActualPlot(G, step, pos):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    nx.draw(G, pos, labels=dict(G.nodes(data='value')), with_labels=True,
            node_color=list(dict(G.nodes(data='color')).values()))
    coordinates = list(zip(*list(pos.values())))
    plt.xlim([min(coordinates[0]) - 0.5, max(coordinates[0]) + 0.5])
    plt.ylim([min(coordinates[1]) - 0.5, max(coordinates[1]) + 0.5])
    fig1.savefig('randomwalk2/rw2_{0:04}.png'.format(step))
    plt.close()


if __name__ == '__main__':
    N = [100, 20]  # number of steps ??????
    n = 5  # number of edges ????????
    randomWalk(n, N[1], 100, 0)
