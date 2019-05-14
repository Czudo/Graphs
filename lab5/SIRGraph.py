import matplotlib.pyplot as plt
import networkx as nx
import random
import subprocess
import numpy as np
import multiprocessing


def SIRGraph(args, name=None):  # Graph, probability and parameter  as tuple: (G,p)
    """
    Function simulates SIR model on a given graph.

    :param args: tuple with 3 parameter: (G, p, temp)
        G - networkx graph: given graph with at least one infected node;
        p - float: a probability of contagion;
        temp - string: can take one of 3 values:
            'infected', 'properties' or 'plot'.

    :param name - string: name of graph, used as name of .png and .gif files where plots of graphs will be saved
        (needed only if temp=='plot')

    :return: depending on temp parameter:
        -if temp=='infected', then function return list of fraction of infected nodes at every time t
        -if temp=='properties', then function return list with 3 properties:
            -total proportion of the network that becomes infected,
            -the time to clear infection,
            -the time to the largest number of infected nodes
        -if temp=='plot', then function save plots of graph at every step as name_step.png, then create .gif file
    """

    G = args[0]
    p = args[1]
    temp = args[2]

    # get list of nodes with 'status' 'infected'
    infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']

    step = 0
    infectedNodes = np.zeros(50)
    infectedNodes[step] = len(infected)
    if temp == 'plot':
        pos = nx.spring_layout(G)
        saveActualPlot(G, step, pos, name)

    while infected:
        for i in infected:
            neighbours = list(G.neighbors(i))

            # random numbers for every neighbour
            U = np.random.random(len(neighbours)).tolist()
            for x in range(1, len(neighbours)):
                if U[x] <= p and G.node[neighbours[x]]['status'] == 'S':
                    G.node[neighbours[x]]['status'] = 'I'
                    G.node[neighbours[x]]['color'] = 'red'

            # set checked infected node as 'reduced'
            G.node[i]['status'] = 'R'
            G.node[i]['color'] = 'grey'
        step = step + 1

        if temp == 'plot':
            saveActualPlot(G, step, pos, name)

        # get list of nodes with 'status' 'infected' in next step of time
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
        return [len(recovered) / len(list(G.nodes())), step, list(infectedNodes).index(max(infectedNodes))]


def fractionOfInfected(N):
    """
    Function saves plot of the fraction of infected nodes in the network at each time t
    [for 4 different graphs generated by createGraph() function].

    :param N: number of nodes in one graph
    :return:
    """
    consideredGraphs = getRandomGraphs(N, 0)  # generate exemplary graphs
    for k in consideredGraphs:
        name = k[0]
        G = k[1]

        # set to all nodes status 'susceptible'
        nx.set_node_attributes(G, 'S', 'status')
        nx.set_node_attributes(G, 'blue', 'color')

        # choose randomly first infected node and set status 'infected'
        vertex = random.choice(list(G.nodes()))
        G.node[vertex]['status'] = 'I'
        G.node[vertex]['color'] = 'red'
        p = [0.5, 0.7, 0.9]
        multiprocess = multiprocessing.Pool()
        fig1 = plt.figure()
        for j in p:
            graphs = [(G.copy(), j, 'infected') for i in range(0, 10**3)]
            a = multiprocess.map(SIRGraph, graphs)
            a = np.mean(np.asarray(a), axis=0)
            plt.plot([i for i in range(0, len(a))], a, label=r'$p=$'+str(j))
        plt.xlabel("time t")
        plt.ylabel("fraction of infected nodes at time t")

        plt.legend()
        fig1.savefig(name + '/fractionOfInfected_' + str(name))


def properties(N):
    """
    Function saves plot of 3 properties [for 4 different graphs generated by createGraph() function]:
    -total propotion of the network that becomes infected,
    -the time to clear infection,
    -the time to the largest number of infected nodes.
    These propeties are dependent on probablity p.

    :param N: number of nodes in one graph
    :return:
    """

    consideredGraphs = getRandomGraphs(N, 0)  # create 4 graphs
    for k in consideredGraphs:  # for every of created graph
        name = k[0]
        G = k[1]
        # set to all nodes status 'susceptible'
        nx.set_node_attributes(G, 'S', 'status')
        nx.set_node_attributes(G, 'blue', 'color')

        p = np.linspace(0.01, 0.99, 20)  # list of probabilities
        multiprocess = multiprocessing.Pool()
        graphs = [(G.copy(), i) for i in p]  # set tuples with considered graph and every probability
        listOfProperties = multiprocess.map(_properties, graphs)  # multiprocess for every pair of graph and probability
        totalInfected, timeToClear, timeOfMaxInfected = list(zip(*listOfProperties))

        fig1 = plt.figure()
        plt.plot(p, totalInfected, label="the total proportion of the network that becomes infected")
        plt.plot(p, timeToClear, label="the time to clear infection")
        plt.plot(p, timeOfMaxInfected, label="the time to the largest number of infected nodes")

        plt.xlabel("probability p")
        plt.ylabel("function dependent on p")
        plt.ylim((-0.2, max(totalInfected + timeToClear + timeOfMaxInfected)+4))
        plt.legend()
        fig1.savefig(name + '/properties_' + str(name))

def _properties(args):
    G = args[0]
    p = args[1]
    listOfProperties = []
    for i in range(0, 10**3):
        # work on copy, not on original graph
        H = G.copy()

        # choose randomly first infected node and set status 'infected'
        vertex = random.choice(list(G.nodes()))
        H.node[vertex]['status'] = 'I'
        H.node[vertex]['color'] = 'red'
        listOfProperties.append(SIRGraph((H, p, 'properties'), name=None))

    return np.mean(np.asarray(listOfProperties), axis=0).tolist()


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


def createGIF(N):
    G, = getRandomGraphs(N, 0.6)
    for i in G:
        nx.set_node_attributes(i[1], 'S', 'status')
        nx.set_node_attributes(i[1], 'blue', 'color')

        # get randomly first infected node and set status 'infected'
        vertex = random.choice(list(i[1].nodes()))
        i[1].node[vertex]['status'] = 'I'
        i[1].node[vertex]['color'] = 'red'
        SIRGraph((i[1], i[2], 'plot'), i[0])


def getRandomGraphs(N, p):
    """
    Function creates random graphs: Erdos-Renyi - 'er', Watts–Strogatz - 'ws', Barabassi-Albert - 'ba'
    :param N: integer, number of nodes
    :param p: float, a probability of contagion
    :return: list of tuples: (name of graph, graph, probability p)
    """
    return [('2d', nx.grid_graph(dim=[np.floor(int(np.sqrt(N))), np.ceil(int(np.sqrt(N)))]), p),
            ('er', nx.gnm_random_graph(N, 3*N), p),
            ('ws', nx.watts_strogatz_graph(N, 4, N/10), p),
            ('ba', nx.barabasi_albert_graph(N, 3), p)]


if __name__ == '__main__':
    #fractionOfInfected(100)
    properties(100)
    #createGIF(30)

