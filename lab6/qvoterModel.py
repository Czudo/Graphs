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


def magnetizationOfTime(n, N, args):
    p = [0.3, 0.4, 0.5]  # probability of independence
    pLegend = ['$p=0.3$', '$p=0.4$', '$p=0.5$']  # lists of strings needed in legend/plot
    colors = ['red', 'blue', 'green']

    q = [3, 4]
    epsilon = 0.01

    multiprocess = multiprocessing.Pool()

    for k in q:
        for tupleGraphs in args:
            name, G = tupleGraphs

            nx.set_node_attributes(G, True, 'spin')  # set starting opinion as True for each spinsons
            plt.figure()

            p1 = [0]*len(p)  # list needed in plots

            # p5 - p7 needed for legend
            p5, = plt.plot([0], color='black', marker='None',
                           linestyle='-', label='dummy-tophead')
            p6, = plt.plot([0], marker='None',
                           linestyle='None', label='dummy-tophead')
            p7, = plt.plot([0], color='black', marker='None',
                           linestyle=':', label='dummy-tophead')

            for j in range(len(p)):
                graphs = [(G.copy(), p[j], k, epsilon, N) for _ in range(n)]
                result = multiprocess.map(modelNN, graphs)
                m = np.mean(np.asarray(result), axis=0)

                p1[j], = plt.plot(np.arange(0, N, 1), m, '-', color=colors[j], label='D ')
                plt.plot(np.arange(0, N, 1), result[1], ':', color=colors[j])

            plt.xlabel("time $t$")
            plt.ylabel("magnetization $<m>$")
            plt.title('Q-voter model, ' + str(name) + r', $q=' + str(k) + r'$, $\epsilon=' + str(epsilon) + '$')

            legend = plt.legend([p5, p7, p6, p1[0], p1[1], p1[2]],
                              ['averaged', 'single run', ''] + pLegend, loc=1, ncol=2)

            plt.gca().add_artist(legend)
            plt.ylim([0.3, 1.05])
            temp = replaceChars(name)
            plt.savefig('magnetizationOfTime_' + str(k) + '_' + str(temp) + '.png')


def replaceChars(string):

    string = string.replace('(', '_')
    string = string.replace(')', '')
    string = string.replace(' ', '_')
    string = string.replace(',', '_')
    return string


def magnetizationOfP(n, N, args):
    p = np.arange(0, 0.5, 0.02)  # probability of independence
    q = [3, 4]
    epsilon = 0.01

    WS = []

    multiprocess = multiprocessing.Pool()
    for k in q:
        fig = plt.figure()

        for tupleGraphs in args:
            name, G = tupleGraphs
            nx.set_node_attributes(G, True, 'spin')
            m = np.zeros(len(p))
            for j in range(len(p)):
                graphs = [(G.copy(), p[j], k, epsilon, N) for _ in range(n)]
                result = multiprocess.map(modelNN, graphs)
                m[j] = np.mean(result)

            if name == 'WS(100,4,0.01)':
                WS.append((m, k))

            plt.plot(p, m, label=name)

        plt.xlabel("independence factor $p$")
        plt.ylabel("magnetization $<m>$")
        plt.title('Q-voter model, $q=' + str(k) + r'$, $\epsilon=' + str(epsilon) + '$')
        plt.legend()
        fig.savefig('magnetizationOfP_' + str(k) + '.png')

    fig = plt.figure()

    for plotList in WS:
        plt.plot(p, plotList[0], label='$q=' + str(plotList[1]) + '$')

    plt.xlabel("independence factor $p$")
    plt.ylabel("magnetization $<m>$")
    plt.title('Q-voter model, WS(100,4,0.01)')
    plt.legend()
    fig.savefig('magnetizationOfP_WS_100_4_0.01.png')


def modelNN(args):
    G, p, q, epsilon, n = args
    m = np.zeros(n)
    m[0] = np.mean(list(nx.get_node_attributes(G, 'spin').values()))  # save actual averaged magnetization to list

    for i in range(1, n):
        spinson = random.choice(list(G.nodes()))  # get randomly spinson

        if random.random() <= p:  # if spinson is independent
            if random.random() <= 1/2:
                G.node[spinson]['spin'] = not G.node[spinson]['spin']  # change his opinion with probability 1/2

        else:
            neighbors = list(G.neighbors(spinson))
            chosen = random.choices(neighbors, k=q)  # get randomly q neighbours of chosen spinson
            listOfSpins = [G.node[x]['spin'] for x in chosen]

            if len(set(listOfSpins)) == 1:  # if spins of chosen neighbors are the same
                G.node[spinson]['spin'] = listOfSpins[0]

            else:
                if random.random() <= epsilon:  # change opinion with probability epsilon
                    G.node[spinson]['spin'] = not G.node[spinson]['spin']

        m[i] = np.mean(list(nx.get_node_attributes(G, 'spin').values()))  # save actual averaged magnetization to list
    return m


if __name__ == '__main__':
    G = getRandomGraphs(100)
    n = 10**2  # number of independent runs
    N = 10**3  # number of MC steps
    magnetizationOfTime(n, N, G)
    magnetizationOfP(n, N, G)
