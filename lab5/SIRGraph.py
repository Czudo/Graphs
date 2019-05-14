import matplotlib.pyplot as plt
import networkx as nx
import math
import random
import subprocess
import numpy as np
import multiprocessing


def SIRGraph(args):
    name = args[0]
    G = args[1]
    p = args[2]
    # set to all nodes status 'susceptible'
    nx.set_node_attributes(G, 'S', 'status')
    nx.set_node_attributes(G, 'blue', 'color')
    # get randomly first infected node and set status 'infected'
    vertex = random.choice(list(G.nodes()))
    G.node[vertex]['status'] = 'I'
    G.node[vertex]['color'] = 'red'
    # list of nodes with 'status' 'infected'
    infected = [x for x,y in G.nodes(data=True) if y['status']=='I']
    step=0
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
        saveActualPlot(G, step, pos, name)
        infected = [x for x, y in G.nodes(data=True) if y['status'] == 'I']


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

def getRandomGraph():
    # [2d lattice, Erdos-Renyi, Watts–Strogatz, Barabassi-Albert]
    return [('2d', nx.grid_graph(dim=[10, 10]), 0.6), ('er', nx.gnm_random_graph(100, 25), 0.6),
            ('ws', nx.watts_strogatz_graph(100, 5, 0.3), 0.6), ('ba', nx.barabasi_albert_graph(100, 5), 0.6)]


if __name__ == '__main__':
    N = 100
    name = ['2d', 'er', 'ws', 'ba']
    G = getRandomGraph()

    #SIRGraph([G[0],G[1],0.6])
    # that two line is for doing SIRGraph concurent for every type of graph
    p = multiprocessing.Pool()
    a = p.map(SIRGraph, G)
    #print(a)
