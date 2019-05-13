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

    # set to all nodes status 'susceptible'
    nx.set_node_attributes(G, 'S', 'status')
    # get randomly first infected node and set status 'infected'
    vertex = random.choice(list(G.nodes()))
    G.node[vertex]['status'] = 'I'

    tostop = [vertex]  # idk what i wanted with that but it can be useful

    # list of (node, status)
    x = list(G.nodes(data='status'))
    nodes, status = list(zip(*x))

    return (status, name)


def getRandomGraph():
    # [2d lattice, Erdos-Renyi, Watts–Strogatz, Barabassi-Albert]
    return [('2d', nx.grid_graph(dim=[10, 10])), ('er', nx.gnm_random_graph(100, 25)),
            ('ws', nx.watts_strogatz_graph(100, 5, 0.3)), ('ba', nx.barabasi_albert_graph(100, 5))]


if __name__ == '__main__':
    N = 100
    name = ['2d', 'er', 'ws', 'ba']
    G = getRandomGraph()

    # that two line is for doing SIRGraph concurent for every type of graph
    p = multiprocessing.Pool()
    a = p.map(SIRGraph, G)
    print(a)
