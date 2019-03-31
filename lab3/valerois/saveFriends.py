from urllib.request import urlopen
import bs4
import re
import csv


def clearText(urlText):
    urlText = re.sub("\n", "", urlText)  # cleaning the text from web page
    urlText = re.sub("<", "", urlText)
    urlText = re.sub(">", "", urlText)
    urlText = urlText.split()  # from string to list
    del urlText[0:13]
    return urlText


if __name__ == "__main__":
    connections = []
    name = "valerois"
    level = 3
    for k in range(0, level+1):
        if k == 0:
            friends = [name]
        else:
            friends = friendsOfFriends
        for i in friends:
            url = "https://www.livejournal.com/misc/fdata.bml?user="+str(i)
            html = urlopen(url)
            soup = bs4.BeautifulSoup(html, 'lxml')
            friendsOfFriends = clearText(str(soup.get_text()))
            for j in friendsOfFriends:
                if ((i, j) not in connections) and ((j, i) not in connections):
                    connections.append((i, j))

    with open("friends.csv", 'w') as csvFile:
        wr = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        wr.writerows(connections)
