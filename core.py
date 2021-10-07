import requests
from bs4 import BeautifulSoup

url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0"
headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'xsadx'}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

#data = soup.find('t', {'class': 'clamp-list'}).find_all('tr')
data = soup.find_all('td', class_='clamp-summary-wrap')


num = 1
for x in data:
    # print(num, x.find('a', class_='title').h3.text)  names passed
    # print(num, x.find('div', class_='metascore_w large game positive').text) metascore passed
    # v = x.find_all('a', class_='metascore_anchor') userscore passed
    # print(num, v[2].div.text)
    # print(num, x.find('span', class_='data').text.strip()) platform passed
    num+=1
