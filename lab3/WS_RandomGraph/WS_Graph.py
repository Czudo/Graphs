from lab3.Graph import Graph
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import signal

class WSGraph(Graph):
    def __init__(self, N, k, beta):
        super().__init__()
        self.N = N
        self.k = k
        self.beta = beta

        for i in range(1, N + 1):
            self.addVertex(i)
        vertices = 2 * self.getVertices()
        for j in range(1, int(k / 2 + 1)):
            for i in range(1, N + 1):
                self.addEdge(vertices[i], vertices[i + j])
        links = int(N * (k / 2))
        vertices = self.getVertices()
        edges = self.getEdges()
        U = np.random.random(links)
        for i in range(0, len(U)):
            if U[i] <= beta:
                edge = edges[i]
                posVert = list(set(vertices) - set(self.getNeighbours(edge[0])) - set([edge[0]]))
                self.deleteEdge(edge[0], edge[1])
                if posVert:
                    toAdd = random.choice(posVert)
                    self.addEdge(edge[0], toAdd)
                else:
                    posVert = list(set(vertices) - set(self.getNeighbours(edge[1])) - set([edge[1]]))
                    toAdd = random.choice(posVert)
                    self.addEdge(edge[1], toAdd)

    def deleteEdge(self, fromVert, toVert):
        if self.vertices[toVert] in self.vertices[fromVert].neighbours: #if given conection exists
            del self.vertices[fromVert].neighbours[self.vertices[toVert]]
            del self.vertices[toVert].neighbours[self.vertices[fromVert]]

    def plotDegrees(self):
        degrees = self.getDegrees()
        plt.figure()
        x = [i for i in range(min(degrees), max(degrees)+1)]
        plt.hist(degrees, density=True, bins=x, label='empirical')

        #plt.plot(x, binom.pmf(x, self.N, self.p), '-o', ms=2, label='binom pmf')
        #plt.plot(x, poisson.pmf(x, self.N*self.p), '-o', ms=2, label='poisson pmf')
        plt.legend()
        plt.savefig('WS_' + str(self.N) + '_' + str(self.k) + '_' + str(self.beta) + '.png')

    def saveGraphProperties(self):
        file = open('WS_' + str(self.N) + '_' + str(self.k) + '_' + str(self.beta) + '.txt', 'w+')
        file.write('WS GRAPH WITH DIRAC DELTA FUNCTION, N=' + str(self.N) + ', k=' + str(self.k) + ', beta=' + str(self.beta) +
                   '\n\nNUMBER OF VERTICES \n' + str(len(self.getVertices())) + '\n' + 'NUMBER OF EDGES \n' +
                   str(len(self.getEdges())) + '\n' + 'AVERAGE DEGREE \ntheoretical:' + str(self.N ) +
                   ', empirical:' + str(np.mean(self.getDegrees())) +
                   '\n' + 'VARIANCE OF THE DEGREE \ntheoretical: ' + str(self.N ) +
                   ', empirical:' + str(np.var(self.getDegrees())))
        file.close

    def getDegrees(self):
        degrees = []
        for i in self.vertices:
            degrees.append(len(self.getNeighbours(i)))
        return degrees

if __name__ == "__main__":
    ws = WSGraph(10, 6, 0.6)
    ws.plotDegrees()
    #ws.saveGraphProperties()

