import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.ticker import MultipleLocator
import random
import subprocess
from matplotlib import patches


def initRandomWalk(n, N):
    G = nx.grid_graph(dim=[N, N])
    nodes = list(G.nodes())
    [x, y] = list(zip(*nodes))  #
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    spacing = 1
    minorLocator = MultipleLocator(spacing)
    ax1.xaxis.set_minor_locator(minorLocator)
    ax1.yaxis.set_minor_locator(minorLocator)
    ax1.grid(which='minor', axis='both')
    plt.xlim([min(x)-0.5, max(x)+0.5])
    plt.ylim([min(y)-0.5, max(y)+0.5])
    start = (round(N/2), round(N/2))  # start at middle of plot
    RandomWalk(n, fig1, ax1, G, start)


def RandomWalk(n, fig1, ax1, G, start):

    ax1.add_patch(
        patches.Circle(start, 0.1, color='r')  # add dot as start position
    )
    fig1.savefig('randomWalk_{}_{}.png'.format(N, 0))
    for i in range(1, n+1):

        ax1.add_patch(
            patches.Circle(start, 0.11, color='w')  # cover starting position with white dot
        )

        listOfNext = list(G.neighbors(start))

        index = random.randint(0, len(listOfNext)-1)
        next = listOfNext[index]
        ax1.add_patch(
            patches.Circle(next, 0.1, color='r')  # add dot at actual position on plot
        )
        colors = nx.get_edge_attributes(G, 'color')

        if (start, next) in list(colors.keys()):
            if colors[(start, next)] != 0:
                color = colors[(start, next)]-20
                nx.set_edge_attributes(G, {(start, next): {'color': color}})
            else:
                color = colors[(start, next)]
                nx.set_edge_attributes(G, {(start, next): {'color': color}})

        elif (next, start) in list(colors.keys()):
            if colors[(next, start)] != 0:
                color = colors[(next, start)]-20
                nx.set_edge_attributes(G, {(next, start): {'color': color}})
            else:
                color = colors[(next, start)]
                nx.set_edge_attributes(G, {(next, start): {'color': color}})
        else:
            color = 120
            nx.set_edge_attributes(G, {(start, next): {'color': color}})

        ax1.plot([start[0], next[0]], [start[1], next[1]], color=(color/255, color/255, color/255))
        fig1.savefig('randomWalk_{}_{}.png'.format(N, i))
        start = next

    files = ['randomWalk_{}_{}.png'.format(N, i) for i in range(0, n+1)]

    cmd = ['magick', 'convert', '-delay', '20', '-loop', '0'] + files + ['randomWalk_{}.gif'.format(N)]
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    N = 20
    n = 200
    initRandomWalk(n, N)
