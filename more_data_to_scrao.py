import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.options.mode.chained_assignment = None
headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'xasd'}

def get_data(data):
    result = []
    for x in data:
        if isinstance(x, list):
            result.append(x[0])
        else:
            result.append(x)
    return result

data = pd.read_csv('final_dataset.csv')[:10]
clear_data = data[['name_game']]
clear_data['platform'] = get_data(data['platform'])

feature_data = pd.DataFrame(columns={
                                'developer',
                                'genre',
                                'type',
                                'rating'
                            })

dev = []
gen = []
typ = []
rat = []


for index, row in clear_data.iterrows():
    name_game = row['name_game'].lower().replace(':', '').replace(',', '').split()
    name_game = '-'.join(name_game)
    platform = '-'.join(row['platform'].lower().split())
    urla = "https://www.metacritic.com/game/" + platform + '/' + name_game
    result = requests.get(urla, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")


    developer = soup.find('li', class_='summary_detail developer').find('span', class_='data').a.text
    dev.append(developer)

    genre = soup.find('li', class_='summary_detail product_genre').find('span', class_='data').text.split()
    gen.append(genre)

    if  soup.find('li', class_='summary_detail product_players'):
        multiplayer = soup.find('li', class_='summary_detail product_players').find('span', class_='data').text


        if 'no' in multiplayer.lower() or '1 player' in multiplayer.lower():
            # print('singleplayer')
            typ.append('singleplayer')
        else:
            # print('multiplayer')
            typ.append('multiplayer')
    else:
        typ.append('NaN')



    if soup.find('li', class_='summary_detail product_rating'):
        rating = soup.find('li', class_='summary_detail product_rating').find('span', class_ ='data').text
        rat.append(rating)
    else:
        rat.append('NaN')



feature_data = pd.DataFrame({
                                'developer': dev,
                                'genre': gen,
                                'type': typ,
                                'rating': rat
                            })

print(feature_data)




