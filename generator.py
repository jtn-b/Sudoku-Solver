import requests
from bs4 import BeautifulSoup
import unicodedata


def getPuzzle():
    data = requests.get('http://www.menneske.no/sudoku/eng/random.html?diff=4')
    soup = BeautifulSoup(data.text, 'html.parser')
    data = []
    for tr in soup.find_all('tr', {'class': 'grid'}):
        row = [td.text for td in tr.find_all('td')]
        data.append(row)
    blank = "\xa0"
    for i in range(9):
        for j in range(9):
            if data[i][j] == blank:
                data[i][j] = "0"
    return data
