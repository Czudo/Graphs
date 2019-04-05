from lab3.Graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import itertools
import scipy.stats as stats


class BAGraph(Graph):
    def __init__(self, N, m0, m):
        super().__init__() # constructor of parent class (Graph())
        self.N = N
        self.m0 = m0
        self.m = m
        self.a = 0
        self.b = 0

        vertices = [i for i in range(1, m0 + 1)]
        edges = [i for i in itertools.combinations(vertices, 2)]  # all posible conections
        self.addEdgesFromList(edges)

        for i in range(m0+1, N+1):
            for j in range(m):
                if i not in self.vertices:
                    self.addVertex(i)
                vertices = self.getVertices()
                degrees = self.getDegrees()
                max = sum(degrees)
                posibleVerts = list(set(vertices) - set(self.getNeighbours(i)) - set([i])) # posible vertices that we can connect with ith vertex
                while True:
                    newVert = np.random.choice(vertices, 1, p=np.divide(degrees, max))[0]
                    if newVert in posibleVerts: # if newVert can be new neighbour, exit from loop
                        break
                self.addEdge(i, newVert)

    def plotDegrees(self):
        degrees = list(self.getDegrees())
        plt.figure()

        [unique, counts] = np.unique(np.sort(degrees), return_counts=True)

        # get only 60% of data (excluding outliers)
        x = np.log10(unique[0:int(0.6*len(unique))])
        y = np.log10(counts[0:int(0.6*len(counts))] / sum(counts))

        # get parameters for linear least-squares regression
        self.a = (stats.linregress(x, y))[0]
        self.b = (stats.linregress(x, y))[1]

        x = [i for i in range(min(degrees), max(degrees) + 1)]
        plt.hist(degrees, density=True, bins=x, label='empirical')

        plt.plot(x, x**self.a*10**self.b, 'g', label='Power law')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('degree')
        plt.ylabel('frequency')
        plt.legend()
        plt.savefig('BA_' + str(self.N) + '_' + str(self.m0) + '_' + str(self.m) + '.png')

    def saveGraphProperties(self):
        file = open('BA_' + str(self.N) + '_' + str(self.m0) + '_' + str(self.m) + '.txt', 'w+')
        file.write('BA GRAPH WITH POWER-LAW DISTRIBUTION, N='
                   + str(self.N) + ', m0=' + str(self.m0) + ', m=' + str(self.m)
                   + '\nf(x)=x**' + str(round(self.a, 2)) + '*10**' + str(round(self.b, 2))
                   + '\n\nNUMBER OF VERTICES ' + str(len(self.getVertices()))
                   + '\n' + 'NUMBER OF EDGES ' + str(len(self.getEdges()))
                   + '\n' + 'AVERAGE DEGREE ' + str(np.mean(self.getDegrees()))
                   + '\n' + 'VARIANCE OF THE DEGREE ' + str(np.var(self.getDegrees())))
        file.close

    def getDegrees(self):
        degrees = []
        for i in self.vertices:
            degrees.append(len(self.getNeighbours(i)))
        return degrees


if __name__ == "__main__":
    ba = BAGraph(2000, 2, 2)
    ba.plotDegrees()
    ba.saveGraphProperties()
