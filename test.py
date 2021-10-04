import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"Accept-Language": "en-US, en;q=0.5"}

url_50 = 'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&ref_=adv_prv'
results_50 = requests.get(url_50, headers=headers)

soup_50 = BeautifulSoup(results_50.text, "html.parser")

url_100 = 'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&start=51&ref_=adv_nxt'
results_100 = requests.get(url_100, headers=headers)
soup_100 = BeautifulSoup(results_100.text, "html.parser")

data_50 = soup_50.find_all('div', class_="lister-item mode-advanced")
data_100 = soup_100.find_all('div', class_="lister-item mode-advanced")


def scraper(data):
    titles = []
    years = []
    time = []
    imdb_ratings = []
    metascores = []
    votes = []
    us_gross = []

    for x in data:
        # name
        name = x.h3.a.text
        titles.append(name)

        # year
        year = x.h3.find('span', class_='lister-item-year text-muted unbold').text
        years.append(year[1:-1])

        # time
        times = x.p.find('span', class_='runtime').text
        time.append(times.split()[0])

        # imdbRatings
        score = x.strong.text
        imdb_ratings.append(score)

        # metascore
        meta_score = x.find('span', class_='metascore').text if x.find('span', class_='metascore') else 'NaN'
        metascores.append(meta_score)

        # votes&us_grossMillions
        voteAndGross = x.find('p', class_='sort-num_votes-visible').find_all('span', attrs={'name': 'nv'})
        vote = voteAndGross[0].text
        votes.append(vote)

        gross = voteAndGross[1].text if len(voteAndGross) > 1 else 'NaN'
        us_gross.append(gross)

    movies = pd.DataFrame({
        'movie': titles,
        'year': years,
        'timeMin': time,
        'imdb': imdb_ratings,
        'metascore': metascores,
        'votes': votes,
        'us_gross': us_gross,
    })

    return movies


d = scraper(data_50).append(scraper(data_100)).reset_index(drop=True)
d.to_csv('movie.csv')
