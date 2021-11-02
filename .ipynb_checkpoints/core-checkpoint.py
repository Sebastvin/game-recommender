import requests
from bs4 import BeautifulSoup
import pandas as pd

<<<<<<< HEAD
headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'dada'}
=======
headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'xasd'}
>>>>>>> 9b3c74378f2f980830ebcb9a6cb5791636b0e686
url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0"
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.text, "html.parser")
num_pages = int(soup.find('li', class_='page last_page').a.text)


def scraper(pages, head):
<<<<<<< HEAD
=======

    d = pd.DataFrame(columns=[
                'name_game',
                'meta_score',
                'user_score',
                'platform',
                'release_date',
                'description']
            )


>>>>>>> 9b3c74378f2f980830ebcb9a6cb5791636b0e686
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

<<<<<<< HEAD
=======

>>>>>>> 9b3c74378f2f980830ebcb9a6cb5791636b0e686
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

<<<<<<< HEAD
    games = pd.DataFrame({
        'name_game': name,
        'meta_score': meta_score,
        'user_score': user_score,
        'platform': platform,
        'release_date': release_date,
        'description': description,
    })

    return games


games = scraper(1, headers).reset_index()
games.to_csv('test_games.csv')
=======
            final_data = pd.DataFrame({
                'name_game': name,
                'meta_score': meta_score,
                'user_score': user_score,
                'platform': platform,
                'release_date': release_date,
                'description': description,
            })

        d = d.append(final_data, ignore_index=True)



    return d

#print(scraper(num_pages, headers))
#games = scraper(num_pages, headers)


#games.to_csv('dataset_games.csv')


games = scraper(1, headers).reset_index(drop=True, inplace=False)
games.to_csv('test_games.csv', index=False)

>>>>>>> 9b3c74378f2f980830ebcb9a6cb5791636b0e686
