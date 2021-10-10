import requests
from bs4 import BeautifulSoup
import pandas as pd

<<<<<<< HEAD
url = "https://www.rottentomatoes.com/top/bestofrt/"

f = requests.get(url)
soup = BeautifulSoup(f.content, 'lxml')                         # create object BeautifulSoup specify parser
movies = soup.find('table', {'class': 'table'}).find_all('a')   # <table class="table">
movies_lst = []
num = 0

for anchor in movies:
                                                               # # # # # # # # # # # # # # # # # # # # # #
    urls = 'https://www.rottentomatoes.com' + anchor['href']    # info needed to take a movie description #
    movies_lst.append(urls)                                     # ex. <a href="/m/it_happened_one_night"  #
    num += 1                                                    # # # # # # # # # # # # # # # # # # # # # #
    movie_url = urls
    movie_f = requests.get(movie_url)
    movie_soup = BeautifulSoup(movie_f.content, 'lxml')
    movie_content = movie_soup.find('div', {'class': 'movie_synopsis clamp clamp-6 js-clamp'})
    print(num, urls, '\n', 'Movie:' + anchor.string.strip())
    print('Movie info:' + movie_content.string.strip())
=======
headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'dada'}
url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0"
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.text, "html.parser")
num_pages = int(soup.find('li', class_='page last_page').a.text)


def scraper(pages, head):
    for num_page in range(0, pages):
        urls = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=" + str(num_page)
        results = requests.get(urls, headers=head)
        soups = BeautifulSoup(results.text, "html.parser")
        data = soups.find_all('td', class_='clamp-summary-wrap')

        name = []
        meta_score = []
        user_score = []
        platform = []
        release_date = []
        description = []

        for x in data:
            # print(num, x.find('a', class_='title').h3.text)  names passed
            title = x.find('a', class_='title').h3.text
            name.append(title)

            # print(num, x.find('div', class_='metascore_w large game positive').text) metascore passed
            score = x.find('a', class_='metascore_anchor').div.text
            meta_score.append(score)

            # userscore = x.find_all('a', class_='metascore_anchor') userscore passed
            # print(num, userscore =[2].div.text)
            user = x.find_all('a', class_='metascore_anchor')[2].div.text
            user_score.append(user)

            # print(num, x.find('span', class_='data').text.strip()) platform passed
            plat = x.find('span', class_='data').text.strip()
            platform.append(plat)

            # data = x.find('div', class_='clamp-details').find_all('span') data passed
            # print(num, data[2].text)
            data = x.find('div', class_='clamp-details').find_all('span')
            release_date.append(data[2].text)

            # print(num, x.find('div', class_='summary').text.strip()) description passed
            text = x.find('div', class_='summary').text.strip()
            description.append(text)

    games = pd.DataFrame({
        'name_game': name,
        'meta_score': meta_score,
        'user_score': user_score,
        'platform': platform,
        'release_date': release_date,
        'description': description,
    })

    return games


games = scraper(num_pages, headers)
games.to_csv('dataset_games.csv')
>>>>>>> 4cd8cfd4594a814a6c1e1f92147b672443a47a40
