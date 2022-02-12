import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml
from ast import literal_eval
import cchardet
import multiprocessing

pd.options.mode.chained_assignment = None


def get_data(new):
    headers = {"Accept-Language": "en-US, en;q=0.5", 'user-agent': 'xasd'}

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

    for index, row in new.iterrows():
        name_game = row['name_game'].lower()
        name_game = name_game.replace(':', '').replace(',', '').replace("'", "").replace('.', '').replace("&",
                                                                                                          '').replace(
            "/", '').replace(';', '').replace('#', '').replace('*', '').replace('~', '').replace('?', '').replace('$',
                                                                                                                  '')
        name_game = name_game.split()
        name_game = '-'.join(name_game)

        urla = "https://www.metacritic.com/game/" + row['platform'][0] + '/' + name_game

        result = requests.get(urla, headers=headers)
        soup = BeautifulSoup(result.content, 'lxml')

        if result.status_code == 200:
            if soup.find('li', class_='summary_detail developer'):

                developer = soup.find('li', class_='summary_detail developer').a.text
                dev.append(developer)
            else:
                dev.append('NaN')
                print(urla)

            if soup.find('li', class_="summary_detail product_genre").findChildren('span', class_='data'):
                genre = soup.find('li', class_="summary_detail product_genre").findChildren('span', class_='data')
                tmp = []
                for x in genre:
                    if x.text not in tmp:
                        tmp.append(x.text)
                gen.append(tmp)
            else:
                gen.append('NaN')
                print(urla)

            if soup.find('li', class_='summary_detail product_players'):
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
                rating = soup.find('li', class_='summary_detail product_rating').find('span', class_='data').text
                rat.append(rating)
            else:
                rat.append('NaN')
        else:
            print(urla)
            dev.append('NaN')
            gen.append('NaN')
            typ.append('NaN')
            rat.append('NaN')

    feature_data = pd.DataFrame({
        'developer': dev,
        'genre': gen,
        'type': typ,
        'rating': rat
    })

    return feature_data


if __name__ == '__main__':
    # working code
    data = pd.read_csv('datasets/final_dataset.csv')
    data.platform = data.platform.apply(literal_eval)
    new_1 = data[['name_game', 'platform']][:1000].copy()  # 1
    new_2 = data[['name_game', 'platform']][1000:2000].copy()  # 2
    new_3 = data[['name_game', 'platform']][2000:3000].copy()  # 3
    new_4 = data[['name_game', 'platform']][3000:4000].copy()  # 4
    new_5 = data[['name_game', 'platform']][4000:5000].copy()  # 5
    new_6 = data[['name_game', 'platform']][5000:6000].copy()  # 6
    new_7 = data[['name_game', 'platform']][6000:7000].copy()  # 7
    new_8 = data[['name_game', 'platform']][7000:].copy()  # 8

    # multiprocessing pool object
    pool = multiprocessing.Pool()

    # pool object with number of element
    pool = multiprocessing.Pool(processes=4)

    # input list
    inputs = [new_1, new_2, new_3, new_4, new_5, new_6, new_7, new_8]

    # map the function to the list and pass
    # function and input list as arguments
    outputs = pool.map(get_data, inputs)

    # Print output list
    result = pd.concat(outputs)

    result.to_csv('datasets/features.csv', index=False)

