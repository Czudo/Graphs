from lab3.Graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import itertools

class BAGraph(Graph):
    def __init__(self, N, m0, m):
        super().__init__()
        self.N = N
        self.m0 = m0
        self.m = m

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
                posibleVerts = list(set(vertices) - set(self.getNeighbours(i)) - set([i]))

                while True:
                    newVert = np.random.choice(vertices, 1, p=np.divide(degrees, max))[0]
                    if newVert in posibleVerts:
                        break
                self.addEdge(i, newVert)


    def plotDegrees(self):
        degrees = list(self.getDegrees())
        plt.figure()
        x = [i for i in range(min(degrees), max(degrees)+1)]
        plt.hist(degrees, density=True, bins=x, label='empirical', log=True)
        plt.xscale('log')

        #plt.plot(x, binom.pmf(x, self.N, self.p), '-o', ms=2, label='binom pmf')
        #plt.plot(x, poisson.pmf(x, self.N*self.p), '-o', ms=2, label='poisson pmf')
        plt.legend()
        plt.savefig('BA_' + str(self.N) + '_' + str(self.m0) + '_' + str(self.m) + '.png')

    def saveGraphProperties(self):
        file = open('BA_' + str(self.N) + '_' + str(self.m0) + '_' + str(self.m) + '.txt', 'w+')
        file.write('BA GRAPH WITH POWER-LAW DISTRIBUTION, N=' + str(self.N) + ', m0=' + str(self.m0) + ', m=' + str(self.m) +
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

    def _getDegrees(self):
        degrees = {}
        for i in self.vertices:
            degrees[i]=len(self.getNeighbours(i))
        return degrees

if __name__ == "__main__":
    ba = BAGraph(2000, 6, 2)
    #print(ba.getVertices())
    ba.plotDegrees()
    #print(ba.getEdges())
    #ba.saveGraph('ba')
    #ba.open('ba')