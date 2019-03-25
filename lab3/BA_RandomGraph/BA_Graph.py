from lab3.Graph import Graph
import itertools
import numpy as np

class BAGraph(Graph):
    def __init__(self, N, p):
        super().__init__()
        vertices = [i for i in range(1, N+1)]
        self.addVerticesFromList(vertices)
        maxLinks = int(N*(N-1)/2)
        weight = np.random.random(maxLinks).tolist()
        edges = [(i) for i in itertools.combinations(vertices, 2)]
        fedges = [edges[x] for x in range(1,N) if weight[x] > p]
        self.addEdgesFromList(fedges)

if __name__=="__main__":
    ba = BAGraph(10, 0.1)
    print(ba.getVertices())
    print(ba.getEdges())
