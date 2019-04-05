from lab3.Graph import Graph
import matplotlib.pyplot as plt
import numpy as np
import random
import math


class WSGraph(Graph):
    def __init__(self, N, k, beta):
        super().__init__()  # constructor of parent class (Graph())
        self.N = N
        self.k = k
        self.beta = beta

        for i in range(1, N + 1):
            self.addVertex(i)
        vertices = 2 * self.getVertices()
        for j in range(1, int(k / 2 + 1)):
            for i in range(1, N + 1):
                self.addEdge(vertices[i], vertices[i + j])  # add start connections
        links = int(N * (k / 2))
        vertices = self.getVertices()
        edges = self.getEdges()
        U = np.random.random(links)
        for i in range(0, len(U)):
            if U[i] <= beta:    # if random number for connection is smaller than beta
                edge = edges[i]
                # list of possible new neighbours (without themselves and their neighbours)
                posVert = list(set(vertices) - set(self.getNeighbours(edge[0])) - set([edge[0]]))
                self.deleteEdge(edge[0], edge[1])  # delete considered connection
                if posVert:  # if possible connection for vertex 'a' exists
                    toAdd = random.choice(posVert) # get randomly new neighbour from list of possible vertices
                    self.addEdge(edge[0], toAdd)
                else:  # if no possible connection for vertex 'a' exists
                    # get possible connection from vertex 'b'
                    posVert = list(set(vertices) - set(self.getNeighbours(edge[1])) - set([edge[1]]))
                    toAdd = random.choice(posVert)  # get randomly new neighbour from list of possible vertices
                    self.addEdge(edge[1], toAdd)

    def deleteEdge(self, fromVert, toVert):
        if self.vertices[toVert] in self.vertices[fromVert].neighbours:  # if given connection exists
            del self.vertices[fromVert].neighbours[self.vertices[toVert]]
            del self.vertices[toVert].neighbours[self.vertices[fromVert]]

    def plotDegrees(self):
        degrees = self.getDegrees()
        plt.figure()
        x = [i for i in range(min(degrees), max(degrees)+1)]
        plt.hist(degrees, density=True, bins=x, label='empirical')

        ytheo = self.toPlot(min(x), max(x))
        plt.plot(x, ytheo, '-', ms=2, label='theoretical')
        plt.legend()
        plt.xlabel('degree')
        plt.ylabel('frequency')
        plt.savefig('WS_' + str(self.N) + '_' + str(self.k) + '_' + str(self.beta) + '.png')

    def toPlot(self, a, b):
        k = [i for i in range(a, b+1)]
        theo = [0] * len(k)
        for i in range(0, len(k)):
            f = min([k[i] - int(self.k/2), int(self.k/2)])
            for j in range(0, f):
                theo[i] = theo[i] + math.factorial(int(self.k/2))/(math.factorial(j)*math.factorial(int(self.k/2)-j))\
                           * (1-self.beta)**j*self.beta**(int(self.k/2)-j) \
                           * (self.beta*int(self.k/2))**(k[i] - int(self.k/2)-j)\
                           / math.factorial(k[i]-int(self.k/2)-j) * math.exp(-self.beta*self.k/2)
        return theo

    def saveGraphProperties(self):
        file = open('WS_' + str(self.N) + '_' + str(self.k) + '_' + str(self.beta) + '.txt', 'w+')
        file.write('WS GRAPH, N=' + str(self.N) + ', k=' + str(self.k) + ', beta=' + str(self.beta)
                   + '\n\nNUMBER OF VERTICES \n' + str(len(self.getVertices()))
                   + '\n' + 'NUMBER OF EDGES \n' + str(len(self.getEdges()))
                   + '\nAVERAGE DEGREE ' + str(np.mean(self.getDegrees()))
                   + '\nVARIANCE OF THE DEGREE ' + str(np.var(self.getDegrees())))
        file.close

    def getDegrees(self):
        degrees = []
        for i in self.vertices:
            degrees.append(len(self.getNeighbours(i)))
        return degrees


if __name__ == "__main__":
    ws = WSGraph(2000, 50, 0.3)
    ws.plotDegrees()
    ws.saveGraphProperties()

