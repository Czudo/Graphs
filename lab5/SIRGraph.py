import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import numpy as np
import multiprocessing


def initSIR(G):
    # set to all nodes status 'susceptible'
    nx.set_node_attributes(G, 'S', 'status')
    nx.set_node_attributes(G, 'blue', 'color')
    # get randomly first infected node and set status 'infected'
    vertex = random.choice(list(G.nodes()))
    G.node[vertex]['status'] = 'I'
    G.node[vertex]['color'] = 'red'
    p = [0.5, 0.7, 0.9]
    multiprocess = multiprocessing.Pool()
    for j in p:
        graphs = [(G.copy(), j) for i in range(1, 10000)]
        a = multiprocess.map(SIRGraph, graphs)
        a = np.mean(np.asarray(a), axis=0)
        plt.plot([i for i in range(0, len(a))], a, label=r'$p=$'+str(j))
    plt.legend()
    plt.show()


def SIRGraph(args, name=None, plot=False):  # Graph and probability as tuple: (G,p)
    G = args[0]
    p = args[1]
    # list of nodes with 'status' 'infected'
    infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']
    step = 0
    infNodes = np.zeros(30)  # trza znaleźć złoty środek :C
    infNodes[step] = len(infected)
    if plot:
        pos = nx.spring_layout(G)
        saveActualPlot(G, step, pos, name)

    while infected:
        for i in infected:
            neighbours = list(G.neighbors(i))
            U = np.random.random(len(neighbours)).tolist()  # random numbers for every neighbour
            for x in range(1, len(neighbours)):
                if U[x] <= p and G.node[neighbours[x]]['status'] == 'S':
                    G.node[neighbours[x]]['status'] = 'I'
                    G.node[neighbours[x]]['color'] = 'red'
            G.node[i]['status'] = 'R'
            G.node[i]['color'] = 'grey'
        step = step+1
        if plot:
            saveActualPlot(G, step, pos, name)
        infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']
        infNodes[step] = len(infected)
    if plot:
        createGIF(name)
    return infNodes


def saveActualPlot(G, step, pos, name):
    fig1 = plt.figure()
    nx.draw(G, pos, labels=dict(G.nodes(data='status')), with_labels=True,
            node_color=tuple(nx.get_node_attributes(G, 'color').values()))
    coordinates = tuple(zip(*tuple(pos.values())))
    plt.xlim([min(coordinates[0])-0.05, max(coordinates[0])+0.05])
    plt.ylim([min(coordinates[1])-0.05, max(coordinates[1])+0.05])
    plt.xlabel('x')
    plt.ylabel('y')
    fig1.savefig(str(name) + '/' + str(name) + '_{0:04}.png'.format(step))
    plt.close()


def createGIF(name):
    cmd = ['magick', 'convert', '-delay', '40', '-loop', '0', str(name) + '/' + str(name) + '_*.png', str(name) + '/' + str(name) + '_gif.gif']
    subprocess.call(cmd, shell=True)


def getRandomGraphs(N, p):
    # [2d lattice, Erdos-Renyi, Watts–Strogatz, Barabassi-Albert]
    # lepsze parametry dla grafów (by ładniejsze wykresy były)
    return [('2d', nx.grid_graph(dim=[int(np.sqrt(N)), int(np.sqrt(N))]), p),
            ('er', nx.gnm_random_graph(N, 400), p),
            ('ws', nx.watts_strogatz_graph(N, 4, 0.3), p),
            ('ba', nx.barabasi_albert_graph(N, 3), p)]


if __name__ == '__main__':
    N = 100
    G = nx.grid_graph(dim=[int(np.sqrt(N)), int(np.sqrt(N))])

    initSIR(G)

