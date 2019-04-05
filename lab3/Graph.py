from graphviz import Source

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


class Vertex:  # class with vertices
    def __init__(self, name):
        self.name = name
        self.neighbours = {}

    def addNeighbour(self,  other,  weight=1):
        self.neighbours[other] = weight

    def getVertNeighbours(self):
        return list(self.neighbours.keys())

    def getWeight(self, other):
        return self.neighbours[other]

    def __str__(self):
        return self.name


class Graph:
    def __init__(self):
        self.vertices = {}

    def addVertex(self, vert):
        new_vert = Vertex(vert)
        self.vertices[vert] = new_vert  # key - name of vertex, value - object from class Vertex

    def addVerticesFromList(self, vertList):
        for vert in vertList:
            self.addVertex(vert)

    def addEdge(self, fromVert, toVert, weight=1):
        if fromVert not in self.vertices.keys():
            self.addVertex(fromVert)
        if toVert not in self.vertices.keys():
            self.addVertex(toVert)
        # if vertex 'a' has 'b' as neighbour, then 'b' has 'a' as neighbour
        self.vertices[fromVert].addNeighbour(self.vertices[toVert], weight)
        self.vertices[toVert].addNeighbour(self.vertices[fromVert], weight)


    def addEdgesFromList(self, edgeList):
        for edge in edgeList:
            if len(edge) == 2:  # if weight is not given then set weight as default
                self.addEdge(edge[0], edge[1])
            else:
                self.addEdge(edge[0], edge[1], edge[2])

    def getVertex(self,  vertKey):
        if vertKey in self.vertices.keys():
            return self.vertices[vertKey]
        else:
            return None

    def getVertices(self):
        return list(self.vertices.keys())

    def getEdges(self):
        list = []
        for k in self.vertices.keys():
            vert = self.vertices[k]
            for n in vert.getVertNeighbours():
                # get only edges above diagonal in connection matrix
                if ((n.name, vert.name, vert.getWeight(self.vertices[n.name])) not in list):
                    list.append((vert.name, n.name,  vert.getWeight(self.vertices[n.name])))
        return list

    def getNeighbours(self, vertKey):
        vert = self.getVertex(vertKey)
        return [neighbour.name for neighbour in vert.getVertNeighbours()]

    def __contains__(self, vert):
        return vert in self.vertices.keys()

    def saveGraph(self, graph):
        with open("results/"+graph+".dot", "w") as f:
            f.write("strict graph{\n")
            for edge in self.getEdges():
                f.write('"'+str(edge[0])+'" -- "'+str(edge[1])+'" [ label = ' + str(edge[2]) + ' ]\n')
            f.write("}")

    def open(self, graph):
        s = Source.from_file("results/"+graph+".dot")
        s.view()
        return

    def getAllPaths(self, fromVert, toVert, path=[]):
        start = self.vertices[fromVert]
        neighbours = start.getVertNeighbours()
        path = path + [start.name]
        if fromVert == toVert:
            return [path]  # if it is the last vertex return path
        elif not neighbours:
            return
        paths = []
        for vertex in neighbours:  # for every neighbour for fromVert
            if vertex.name not in path:  # if vertex wasnt visited
                tempPaths = self.getAllPaths(vertex.name, toVert, path)  # get all paths between vertex and toVert
                for p in tempPaths:
                    paths.append(p)
        return paths

    def _getShortestPaths(self,fromVert, toVert):
        paths = self.getAllPaths(fromVert, toVert)
        weights = []  # list of total weights of paths
        for path in paths:  # for every found path
            weight = 0
            for i in range(len(path)-1):  # count total weight of path
                weight += self.getVertex(path[i]).getWeight(self.getVertex(path[i+1]))
            weights.append(weight)
        if weights:   # if any connection between fromVert and toVert exists, so if weights is not empty list
            index = [i for i, x in enumerate(weights) if x == min(weights)]  # find every path with minimal weight
            to_return = []
            for i in index:
                to_return.append(paths[i])
            return [min(weights), to_return]
        else:
            return [None, None]     # if no connection exists, then set weight and path as None

    def getShortestPaths(self, fromVert):
        vertices = self.getVertices()
        paths = {}
        message = "Shortest paths from vert '" + fromVert + "' to:\n"
        for vert in vertices:
            paths[vert]=self._getShortestPaths(fromVert, vert)
            message += "'" + vert + "': weight=" + str(list(paths[vert])[0]) + ", list of paths: "
            message += str(list(paths[vert])[1]) + "\n"
        with open("results/" + "paths_from_" + fromVert + ".txt", "w") as f:
            f.write(message)
        return message



if __name__=="__main__":

    G = Graph()
    edges=[("Bob", "Gail"), ("Irene", "Gail"),
           ("Gail", "Harry"), ("Irene", "Jen"),
           ("Alice", "David"), ("Harry", "Jen"), ("Ernst", "Frank"),
           ("Alice", "Ernst", 5), ("Jen", "Gail"), ("David", "Carl"),
           ("Alice", "Frank"), ("Harry", "Irene"), ("Carl", "Frank")]

    G.addEdgesFromList(edges)

    print(G.getVertices())
    print(G.getEdges())
    print(G.getNeighbours("Alice"))

    print("Alice" in G)
    print("Paulina" in G)

    print(G.getShortestPaths('Alice'))

    G.saveGraph("testGraph")
    G.open("testGraph")