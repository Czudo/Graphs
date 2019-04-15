import matplotlib.pyplot as plt
import networkx as nx
import math
import random
import subprocess
import numpy as np


def randomWalk(G, N, name):
    degree = list(zip(*G.degree()))
    nodesList = [degree[0][i] for i in range(len(degree)) if degree[1][i] == 0]  # list with vertices with no connection
    start = list(G.nodes() - set(nodesList))[0]  # set start as first vertex with any connection

    hasPath = []  # list of vertices that have at least indirect connection with start
    for i in G.nodes():
        if nx.has_path(G, start, i):  # if exists path from start to i, add i to list
            hasPath.append(i)

    HTimes = []
    copy = [i for i in hasPath]  # copy of hasPath to change them in function randomWalk, not global
    initRandomWalk(G, start, copy, name, plot=True)  # only for one gif of random walk

    for j in range(0, N):  # for calculations, N=100
        copy = [i for i in hasPath]  # work on copy list, not original hasPath
        HTimes.append(initRandomWalk(G, start, copy, name, plot=False))

    HTimes = np.asarray(HTimes)
    HTimes[HTimes == np.inf] = 10000
    HTimes = HTimes.tolist()
    avHTimes = np.mean(HTimes, axis=0)
    maximum = math.ceil(max(avHTimes[avHTimes != 10000]) / 10) * 10
    nodes = list(G.nodes())

    fig1 = plt.figure()
    markerLine, stemLines, baseLine = plt.stem(nodes, avHTimes, linefmt='b')
    plt.setp(stemLines, 'linewidth', '2.0')
    plt.plot([min(nodes), max(nodes)], [maximum, maximum], 'r')  # line that defines infinity
    plt.ylim([-5, maximum+20])
    plt.xlabel('Number of vertex')
    plt.ylabel('Average hitting time')
    fig1.savefig('randomwalk2/avHT_rw2_' + str(name) + '.png')


def initRandomWalk(G, start, toVisit, name, plot=False):
    other = (255/255, 153/255, 230/255)  # RGB color for actual vertex
    actual = (179/255, 0/255, 134/255)  # RGB color for other vertices
    nx.set_node_attributes(G, np.inf, 'value')  # set all vertex value inf and other color
    nx.set_node_attributes(G, other, 'color')

    G.node[start]['value'] = 0  # set start node value 0 and color actual
    G.node[start]['color'] = actual

    if start in toVisit:
        toVisit.remove(start)  # remove start vertex from list with not visited vertices

    if plot:
        pos = nx.spring_layout(G)  # get position of graph nodes
        saveActualPlot(G, 0, pos)

    i = 1
    while toVisit:  # while exists vertex that was not visited but it can be
        posibleVertices = list(G.neighbors(start))
        next = random.choice(posibleVertices)
        if G.node[next]['value'] == np.inf:  # if its first visit in next
            G.node[next]['value'] = i
            toVisit.remove(next)  # remove next vertex from list with not visited vertices

        G.node[start]['color'] = other  # set color of actual vertex as other
        G.node[next]['color'] = actual  # set color of next vertex as actual
        start = next
        if plot:
            saveActualPlot(G, i, pos)
        i = i + 1

    if plot:
        cmd = ['magick', 'convert', '-delay', '40', '-loop', '0', 'randomwalk2/rw2_*.png', 'randomwalk2/gif_rw2_' + str(name) + '.gif']
        subprocess.call(cmd, shell=True)

    if not plot:
        return list(nx.get_node_attributes(G, 'value').values())


def saveActualPlot(G, step, pos):
    fig1 = plt.figure()
    nx.draw(G, pos, labels=dict(G.nodes(data='value')), with_labels=True,
            node_color=tuple(nx.get_node_attributes(G, 'color').values()))
    coordinates = tuple(zip(*tuple(pos.values())))
    plt.xlim([min(coordinates[0])-0.05, max(coordinates[0])+0.05])
    plt.ylim([min(coordinates[1])-0.05, max(coordinates[1])+0.05])
    plt.xlabel('x')
    plt.ylabel('y')
    fig1.savefig('randomwalk2/rw2_{0:04}.png'.format(step))
    plt.close()


def getRandomGraph(name):
    if name == 'er':
        return nx.gnm_random_graph(20, 25)
    elif name == 'ws':
        return nx.watts_strogatz_graph(20, 5, 0.3)
    elif name == 'ba':
        return nx.barabasi_albert_graph(20, 5)
    else:
        exit()  # end program


if __name__ == '__main__':
    N = 100
    name = 'er'  # Erdos-Renyi - 'er', Watts–Strogatz - 'ws', Barabassi-Albert - 'ba'
    G = getRandomGraph(name)
    randomWalk(G, N, name)
