from urllib.request import urlopen
import bs4
import re
import csv

connections = []


def clearText(urlText):
    urlText = re.sub("\n", "", urlText)  # cleaning the text from web page
    urlText = re.sub("<", "", urlText)
    urlText = re.sub(">", "", urlText)
    urlText = urlText.split()  # from string to list
    del urlText[0:13]
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


def saveFriends():
    print(len(connections))
    with open("friends.csv", 'w') as csvFile:
        wr = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        wr.writerows(connections)


if __name__ == "__main__":
    getConnections()
    saveFriends()
