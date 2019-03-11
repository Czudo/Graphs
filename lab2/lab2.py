from graphviz import Source

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/' #without that graphviz didn't work

class GraphVertex():
    def __init__(self, name):
        self.name = name
        self.neighbours = {}

    def addNeighbour(self,  other,  weight=1):
        self.neighbours[other] = weight

    def getNeighbours(self):
        return list(self.neighbours.keys())

    def getWeight(self, other):
        return self.neighbours[other]

    def __str__(self):
        return self.name

class Graph:
    def __init__(self): #
        self.vertices = {}

    def addVertex(self, vert): #
        new_vert = GraphVertex(vert)
        self.vertices[vert] = new_vert

    def addVerticesFromList(self, vertList): #
        for vert in vertList:
            self.addVertex(vert)

    def addEdge(self, fromVert, toVert, weight=1): #
        if fromVert not in self.vertices.keys():
            self.addVertex(fromVert)
        if toVert not in self.vertices.keys():
            self.addVertex(toVert)
        self.vertices[fromVert].addNeighbour(self.vertices[toVert], weight)
        self.vertices[toVert].addNeighbour(self.vertices[fromVert], weight)


    def addEdgesFromList(self, edgeList): #
        for edge in edgeList:
            if len(edge) == 2:
                self.addEdge(edge[0], edge[1])
            else:
                self.addEdge(edge[0], edge[1], edge[2])

    def getVertex(self,  vertKey): #dodatkowe
        if vertKey in self.vertices.keys():
            return self.vertices[vertKey]
        else:
            return None

    def getVertices(self): #
        return list(self.vertices.keys())

    def getEdges(self): #
        list = []
        for k in self.vertices.keys():
            vert=self.vertices[k]
            for n in vert.getNeighbours():
                if ((n.name, vert.name, vert.getWeight(self.vertices[n.name])) not in list):
                    list.append((vert.name, n.name,  vert.getWeight(self.vertices[n.name])))
        return list

    def getNeighbors(self, vertKey): #
        vert = self.getVertex(vertKey)
        return vert.getNeighbours()

    def __contains__(self, vert): #
        return vert in self.vertices.keys()

    def saveGraph(self, graph):
        with open(graph+".dot", "w") as f:
            f.write("strict graph{\n")
            for edge in self.getEdges():
                f.write('"'+str(edge[0])+'" -- "'+str(edge[1])+'" [ label = ' + str(edge[2]) + ' ]\n')
            f.write("}")
        print("done.")

    def open(self, graph):
        s = Source.from_file(graph+".dot")
        s.view()
        return

    def getShortestPath(self,fromVert, toVert):
        paths=self.getAllPaths(fromVert, toVert)
        print(paths)
        weights=[]
        for path in paths:
            weight=0
            for i in range(0,len(path)-1):
                weight += self.getVertex(path[i]).getWeight(self.getVertex(path[i+1]))
            weights.append(weight)
        index=weights.index(min(weights))

        return {weights[index]: paths[index]}

    def getAllPaths(self, fromVert, toVert, path=[]):
        #minimum(values())(koszt przejścia)
        #is values<^
        #jak tak to przechodze (minimal weight=maxint)
        #jak nie to kończę
        start=self.vertices[fromVert]
        neighbours=start.getNeighbours()
        path =  path + [start.name]
        if fromVert == toVert:
            return [path]
        if not neighbours:
            return
        paths = []
        for vertex in neighbours:
            if vertex.name not in path:
                extendedPaths = self.getAllPaths(vertex.name, toVert, path)
                for p in extendedPaths:
                    paths.append(p)
        return paths

    def getShortestPaths(self, fromVert):
        vertices = self.getVertices()
        paths={}
        message="Shortest path from vert " + fromVert +" to:\n_________________________________ \n"
        for vert in vertices:
            if vert!=fromVert:
                paths[vert]=self.getShortestPath(fromVert, vert)
                message+= vert + ": weight=" + str(list(paths[vert].keys())[0]) + ", path: " + str(list(paths[vert].values())[0]) +";\n"
        return message


if __name__ == "__main__":
    G = Graph()
    edges=[("Alice", "Bob"), ("Bob", "Gail"), ("Irene", "Gail"),
           ("Carl", "Alice"), ("Gail", "Harry"), ("Irene", "Jen"),
           ("Alice", "David", 10), ("Harry", "Jen"), ("Ernst", "Frank"),
           ("Alice", "Ernst"), ("Jen","Gail"), ("David", "Carl"),
           ("Alice", "Frank"), ("Harry", "Irene"), ("Carl", "Frank")]
    G.addEdgesFromList(edges)
    #print(G.getVertices())
    #print(G.getEdges())
    print(G.getShortestPaths('Alice'))
    G.saveGraph("testGraph")
    G.open("testGraph")

