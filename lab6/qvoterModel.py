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


def magnetizationOfTime(args):
    p = [0.3, 0.4, 0.5]  # probability of independence
    pLegend = ['$p=0.3$', '$p=0.4$', '$p=0.5$']
    q = [3, 4]
    epsilon = 0.01
    n = 10**3

    colors = ['red', 'blue', 'green']
    multiprocess = multiprocessing.Pool()
    for k in q:
        for tupleGraphs in args:
            name, G = tupleGraphs
            print(name)

            nx.set_node_attributes(G, True, 'spin')
            plt.figure()
            p1 = [0]*len(p)
            p5, = plt.plot([0], color='black', marker='None',
                           linestyle='-', label='dummy-tophead')
            p6, = plt.plot([0], marker='None',
                           linestyle='None', label='dummy-tophead')
            p7, = plt.plot([0], color='black', marker='None',
                           linestyle=':', label='dummy-tophead')

            for j in range(len(p)):
                graphs = [(G.copy(), p[j], k, epsilon) for i in range(n)]
                result = multiprocess.map(modelNN, graphs)
                m = np.mean(np.asarray(result), axis=0)

                p1[j], = plt.plot(np.arange(0, 1000, 1), m, '-', color=colors[j], label='D ')
                plt.plot(np.arange(0, 1000, 1), result[1], ':', color=colors[j])

            plt.xlabel("time $t$")
            plt.ylabel("magnetization $<m>$")
            plt.title('Q-voter model, ' + str(name) + r', $q=' +str(k)+ r'$, $\epsilon=' + str(epsilon) + '$')

            leg4 = plt.legend([p5, p7, p6, p1[0], p1[1], p1[2]],
                              ['averaged', 'single run', ''] + pLegend, loc=1, ncol=2)
            plt.gca().add_artist(leg4)
            plt.ylim([0.3, 1.05])
            temp = name.replace('(', '_')
            temp = temp.replace(')', '')
            temp = temp.replace(' ', '_')
            temp = temp.replace(',', '_')
            plt.savefig('magnetizationOfTime_'+str(k)+'_' + str(temp)+'.png')


def magnetizationOfP(args):
    p = np.arange(0, 0.5, 0.02)  # probability of independence
    q = [3, 4]
    epsilon = 0.01
    n = 10**3
    WS = []
    for k in q:
        fig = plt.figure()
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
        plt.ylabel("magnetization $<m>$")
        plt.title('Q-voter model, $q='+str(k)+r'$, $\epsilon='+str(epsilon)+'$')
        plt.legend()
        fig.savefig('magnetizationOfP_' + str(k))
    fig = plt.figure()
    for plotList in WS:
        plt.plot(p, plotList[0], label='$q='+str(plotList[1])+'$')
    plt.xlabel("independence factor $p$")
    plt.ylabel("magnetization $<m>$")
    plt.title('Q-voter model, WS(100,4,0.01)')
    plt.legend()
    fig.savefig('magnetizationOfP_WS_100_4_0.01.png')


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
    magnetizationOfTime(G)
    # magnetizationOfP(G)
