import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np
import multiprocessing


def getRandomGraphs(N):
    """
    Function creates random graphs

    :param N: integer, number of nodes
    :return: list of tuples: (name of graph, graph)
    """
    return [('complete graph', nx.complete_graph(N)),
            ('WS(100,4,0.01)', nx.watts_strogatz_graph(N, 4, 0.01)),
            ('WS(100,4,0.2)', nx.watts_strogatz_graph(N, 4, 0.2)),
            ('BA(100,4)', nx.barabasi_albert_graph(N, 4))]


def magnetizationOfTime(G):
    p = np.arange(0, 0.5, 0.02)  # probability of independence
    q = 4
    epsilon = 0.01
    n = 10**3

    nx.set_node_attributes(G, True, 'spin')

    graphs = [(G.copy(), p[-1], q, epsilon) for i in range(n)]

    multiprocess = multiprocessing.Pool()
    a = multiprocess.map(modelNN, graphs)

    a = np.mean(np.asarray(a), axis=0)
    plt.figure()
    plt.plot(np.arange(0, 1000, 1), a, label=r'$p=$')
    plt.show()


def magnetizationOfP(args):
    p = np.arange(0, 0.5, 0.02)  # probability of independence
    q = [3, 4]
    epsilon = 0.01
    n = 10**1
    WS = []
    for k in q:
        plt.figure()
        multiprocess = multiprocessing.Pool()
        for tupleGraphs in args:
            name, G = tupleGraphs
            print(name)
            nx.set_node_attributes(G, True, 'spin')

            m = np.zeros(len(p))

            for j in range(len(p)):
                graphs = [(G.copy(), p[j], k, epsilon) for i in range(n)]
                a = multiprocess.map(modelNN, graphs)
                m[j] = np.mean(a)
            if name == 'WS(100,4,0.01)':
                WS.append((m, k))
            plt.plot(p, m, label=name)
        plt.xlabel("independence factor $p$")
        plt.ylabel("avarange magnetization $<m>$")
        plt.title('Q-voter model, $q='+str(k)+r'$, $\epsilon='+str(epsilon)+'$')
        plt.legend()
    plt.figure()
    for list in WS:
        plt.plot(p, list[0], label='$q='+str(list[1])+'$')
    plt.xlabel("independence factor $p$")
    plt.ylabel("avarange magnetization $<m>$")
    plt.title('Q-voter model, WS(100,4,0.01)')
    plt.legend()
    plt.show()


def modelNN(args):
    G, p, q, epsilon = args
    n = 1000
    m = np.zeros(n)
    m[0] = np.mean(list(nx.get_node_attributes(G, 'spin').values()))
    for i in range(1, n):
        spinson = random.choice(list(G.nodes()))
        if random.random() <= p:
            if random.random() <= 1/2:
                G.node[spinson]['spin'] = not G.node[spinson]['spin']
        else:
            neighbors = list(G.neighbors(spinson))
            chosen = random.choices(neighbors, k=q)
            listOfSpins = [G.node[x]['spin'] for x in chosen]
            if len(set(listOfSpins)) == 1:  # if spins of chosen neighbors are the same
                G.node[spinson]['spin'] = listOfSpins[0]
            else:
                if random.random() <= epsilon:
                    G.node[spinson]['spin'] = not G.node[spinson]['spin']

        m[i] = np.mean(list(nx.get_node_attributes(G, 'spin').values()))
    return m


if __name__ == '__main__':
    G = getRandomGraphs(100)
    #G = G[2][1]
    #magnetizationOfTime(G)
    magnetizationOfP(G)
