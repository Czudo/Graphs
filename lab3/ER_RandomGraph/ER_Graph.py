from lab3.Graph import Graph
import itertools
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson


class ERGraph(Graph):
    def __init__(self, N, p):
        super().__init__()  # constructor of parent class (Graph())
        self.N = N
        self.p = p

        vertices = [i for i in range(1, N + 1)]
        self.addVerticesFromList(vertices)
        max = int(N * (N - 1) / 2)  # number of maximum possible connections
        U = np.random.random(max).tolist()  # random numbers for every possible connection
        allEdges = [i for i in itertools.combinations(vertices, 2)]  # list of all possible connections
        edges = [allEdges[x] for x in range(1, max) if U[x] <= p]
        self.addEdgesFromList(edges)

    def plotDegrees(self):
        degrees = self.getDegrees()
        plt.figure()
        x = [i for i in range(min(degrees), max(degrees)+1)]
        plt.hist(degrees, density=True, bins=x, label='empirical')
        plt.plot(x, binom.pmf(x, self.N, self.p), '-o', ms=2, label='binom pmf')
        plt.plot(x, poisson.pmf(x, self.N*self.p), '-', ms=2, label='poisson pmf')
        plt.legend()
        plt.xlabel('degree')
        plt.ylabel('frequency')
        plt.savefig('ER_' + str(self.N) + '_' + str(self.p) + '.png')

    def saveGraphProperties(self):
        file = open('ER_' + str(self.N) + '_' + str(self.p) + '.txt', 'w+')
        file.write('ER GRAPH WITH BINOMIAL DISTRIBUTION, N='
                   + str(self.N) + ', p=' + str(self.p) +
                   '\n\nNUMBER OF VERTICES \n' + str(len(self.getVertices()))
                   + '\n' + 'NUMBER OF EDGES \n' + str(len(self.getEdges()))
                   + '\n' + 'AVERAGE DEGREE \ntheoretical:' + str(self.N * self.p)  # binomal mean = N*p
                   + ', empirical:' + str(np.mean(self.getDegrees()))
                   + '\n' + 'VARIANCE OF THE DEGREE \ntheoretical: '
                   + str(self.N * self.p * (1 - self.p))  # binomal var = N*p*(1-p)
                   + ', empirical:' + str(np.var(self.getDegrees())))
        file.close

    def getDegrees(self):
        degrees = []
        for i in self.vertices:
            degrees.append(len(self.getNeighbours(i)))
        return degrees


if __name__ == "__main__":
    p = [0.1, 0.05, 0.01]
    for i in p:
        er = ERGraph(2000, i)
        er.plotDegrees()
        er.saveGraphProperties()
