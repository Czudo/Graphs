import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.ticker import MultipleLocator
import random
import subprocess
from matplotlib import patches


def initRandomWalk(n, N):
    G = nx.grid_graph(dim=[N, N])
    nodes = list(G.nodes())
    [x, y] = list(zip(*nodes))
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    minorLocator = MultipleLocator(1)  # space between lines in grid
    ax1.xaxis.set_minor_locator(minorLocator)  # set that on x and y axis
    ax1.yaxis.set_minor_locator(minorLocator)
    ax1.grid(which='minor', axis='both')

    plt.xlim([min(x)-0.5, max(x)+0.5])
    plt.ylim([min(y)-0.5, max(y)+0.5])
    plt.xlabel('x')
    plt.ylabel('y')
    start = (round(N/2), round(N/2))  # start at middle of plot (or close to middle)
    RandomWalk(n, fig1, ax1, G, start)


def RandomWalk(n, fig1, ax1, G, start):
    ax1.add_patch(patches.Circle(start, 0.1, color='r'))  # add dot as start position
    fig1.savefig('randomwalk/rw_' + str(N) + '_{0:04}.png'.format(0))

    for i in range(1, n+1):
        posibleVertices = list(G.neighbors(start))
        next = random.choice(posibleVertices)
        ax1.add_patch(patches.Circle(start, 0.15, color='w'))  # cover starting position with white dot
        ax1.add_patch(patches.Circle(next, 0.1, color='r'))  # add dot at actual position on plot

        colors = nx.get_edge_attributes(G, 'color')  # get color attribute for all edges
        color = getColor(G, colors, start, next)

        # plot line between nodes with its color (RGB)
        ax1.plot([start[0], next[0]], [start[1], next[1]], color=(color/255, color/255, color/255))
        fig1.savefig('randomwalk/rw_' + str(N) + '_{0:04}.png'.format(i))  # save current plot
        start = next

    cmd = ['magick', 'convert', '-delay', '20', '-loop', '0', 'randomwalk/rw_'
           + str(N) + '_*.png', 'randomwalk/gif_rw1_' + str(N) + '_' + str(n) + 'steps.gif']
    subprocess.call(cmd, shell=True)


def getColor(G, colors, start, next):
    if (start, next) in list(colors.keys()):  # if connection was visited
        if colors[(start, next)] != 0:  # and if its color is not black
            color = colors[(start, next)] - 20  # set darker color
            nx.set_edge_attributes(G, {(start, next): {'color': color}})
        else:  # if edges color is black
            color = colors[(start, next)]  # set the same color
            nx.set_edge_attributes(G, {(start, next): {'color': color}})
    elif (next, start) in list(colors.keys()):  # else if connection was visited, but from next to start
        if colors[(next, start)] != 0:  # do the same
            color = colors[(next, start)] - 20
            nx.set_edge_attributes(G, {(next, start): {'color': color}})
        else:
            color = colors[(next, start)]
            nx.set_edge_attributes(G, {(next, start): {'color': color}})
    else:  # if its first visit from start to next (or from next to start)
        color = 120  # set light grey
        nx.set_edge_attributes(G, {(start, next): {'color': color}})

    return color


if __name__ == '__main__':
    N = 20  # number of vertices in one dimension
    n = 10  # number of steps
    initRandomWalk(n, N)
