from urllib.request import urlopen
import bs4
import re
import matplotlib.pyplot as plt
import csv
import networkx as nx
import collections

connections = []


def clearText(urlText):
    urlText = re.sub("\n", "", urlText)  # cleaning the text from web page
    urlText = re.sub("<", "", urlText)
    urlText = re.sub(">", "", urlText)
    urlText = urlText.split()  # from string to list
    del urlText[0:13]  # delete first 13 words
    return urlText


def getConnections(name="valerois", lvl=0):
    global connections
    url = "https://www.livejournal.com/misc/fdata.bml?user="+name
    html = urlopen(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    friends = list(set(clearText(str(soup.get_text()))))
    for friend in friends:
        if ((name, friend) not in connections) and ((friend, name) not in connections):
            connections.append((name, friend))
            if lvl < 1:
                getConnections(friend, lvl+1)


def saveToCSV(name, toSave):
    with open(name + ".csv", 'w') as csvFile:
        wr = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        wr.writerows(toSave)


def graph():
    G = nx.Graph()
    with open('friends.csv') as csvfile:
        G.add_edges_from(list(csv.reader(csvfile, delimiter=',')))

    noNodes = G.number_of_nodes()  # checking number of nodes
    noEdges = G.number_of_edges()  # checking number of edges
    saveToCSV('valerois', [['Number of nodes: ' + str(noNodes)], ['Number of edges: ' + str(noEdges)]])

    celebrities = list((collections.OrderedDict(sorted(
                    nx.degree_centrality(G).items(),
                    key=lambda t: t[1], reverse=True
                    ))).items())
    saveToCSV('celebrities', celebrities[0:10])  # save to csv only 10 celebrities

    plt.figure()
    degrees = [val for (node, val) in G.degree()]

    plt.hist(degrees, density=True, bins=10, label='empirical')
    plt.yscale('log')
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.savefig('degree_distribution.png')

    communicationBottlenecks = nx.betweenness_centrality(G, k=6)  # using 6 node sample to estimate betweenness
    communicationBottlenecks = list((collections.OrderedDict(sorted(
                                    communicationBottlenecks.items(),
                                    key=lambda t: t[1]))).items())
    saveToCSV('communication_bottlenecks', communicationBottlenecks)


if __name__ == "__main__":
    # global connections
    # getConnections()
    # saveToCSV('friends', connections)
    graph()
