import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import numpy as np
import multiprocessing


def fractionOfInfected():
    # set to all nodes status 'susceptible'
    G = nx.barabasi_albert_graph(N, 3)
    nx.set_node_attributes(G, 'S', 'status')
    nx.set_node_attributes(G, 'blue', 'color')
    # get randomly first infected node and set status 'infected'
    vertex = random.choice(list(G.nodes()))
    G.node[vertex]['status'] = 'I'
    G.node[vertex]['color'] = 'red'
    p = [0.5, 0.7, 0.9]
    multiprocess = multiprocessing.Pool()
    for j in p:
        graphs = [(G.copy(), j, 'infected') for i in range(1, 10000)]
        a = multiprocess.map(SIRGraph, graphs)
        a = np.mean(np.asarray(a), axis=0)
        plt.plot([i for i in range(0, len(a))], a, label=r'$p=$'+str(j))
    plt.legend()
    plt.show() #zapisać wykresy


def initPr(args):
    G = args[0]
    p = args[1]
    a = []
    for i in range(0, 1000):
        vertex = random.choice(list(G.nodes()))
        H = G.copy()
        H.node[vertex]['status'] = 'I'
        H.node[vertex]['color'] = 'red'
        a.append(SIRGraph((H, p, 'properties'), name=None))
    a = np.mean(np.asarray(a), axis=0)
    return a.tolist()


def properties():
    # set to all nodes status 'susceptible'
    G = nx.barabasi_albert_graph(N, 3)
    nx.set_node_attributes(G, 'S', 'status')
    nx.set_node_attributes(G, 'blue', 'color')

    p = np.linspace(0.01, 0.99, 20)
    multiprocess = multiprocessing.Pool()
    graphs = [(G.copy(), i) for i in p]
    a = multiprocess.map(initPr, graphs)
    totalInfected, timeToClear, timeOfMaxInfected = list(zip(*a))

    plt.plot(p, totalInfected)
    plt.plot(p, timeToClear)
    plt.plot(p, timeOfMaxInfected)
    plt.show() #zapisać wykresy


def SIRGraph(args, name=None):  # Graph and probability as tuple: (G,p)
    G = args[0]
    p = args[1]
    temp = args[2]
    # list of nodes with 'status' 'infected'
    infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']
    step = 0
    infectedNodes = np.zeros(30)  # trza znaleźć złoty środek :C
    infectedNodes[step] = len(infected)
    if temp == 'plot':
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
        if temp == 'plot':
            saveActualPlot(G, step, pos, name)
        infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']
        infectedNodes[step] = len(infected)
    if temp == 'plot':
        cmd = ['magick', 'convert', '-delay', '40', '-loop', '0', str(name) + '/'
               + str(name) + '_*.png', str(name) + '/' + str(name) + '_gif.gif']
        subprocess.call(cmd, shell=True)
    elif temp == 'infected':
        return infectedNodes
    elif temp == 'properties':
        recovered = [x for x, y in G.nodes(data=True) if y['status'] == 'R']
        return [len(recovered)/len(list(G.nodes())), step, list(infectedNodes).index(max(infectedNodes))]


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


def createGIF():
    N = 30
    G = getRandomGraphs(N, 0.6)
    for i in G:
        nx.set_node_attributes(i[1], 'S', 'status')
        nx.set_node_attributes(i[1], 'blue', 'color')
        # get randomly first infected node and set status 'infected'
        vertex = random.choice(list(i[1].nodes()))
        i[1].node[vertex]['status'] = 'I'
        i[1].node[vertex]['color'] = 'red'
        SIRGraph((i[1], i[2], 'plot'), i[0])


def getRandomGraphs(N, p):
    # [2d lattice, Erdos-Renyi, Watts–Strogatz, Barabassi-Albert]
    # lepsze parametry dla grafów (by ładniejsze wykresy były)
    return [('2d', nx.grid_graph(dim=[int(np.floor(np.sqrt(N))), int(np.ceil(np.sqrt(N)))]), p),
            ('er', nx.gnm_random_graph(N, 3*N), p),
            ('ws', nx.watts_strogatz_graph(N, 4, N/10), p),
            ('ba', nx.barabasi_albert_graph(N, 3), p)]


if __name__ == '__main__':
    N = 100
    #fractionOfInfected()
    #properties()
    createGIF()

