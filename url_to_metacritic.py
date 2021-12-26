import pandas as pd
from ast import literal_eval

pd.options.mode.chained_assignment = None


def get_data(new):
    urls = []

    for index, row in new.iterrows():
        name_game = row['name_game'].lower()
        name_game = name_game.replace(':', '').replace(',', '').replace("'", "").replace('.', '').replace("&",
                                                                                                          '').replace(
            "/", '').replace(';', '').replace('#', '').replace('*', '').replace('~', '').replace('?', '').replace('$',
                                                                                                                  '')
        name_game = name_game.split()
        name_game = '-'.join(name_game)

        urla = "https://www.metacritic.com/game/" + row['platform'][0] + '/' + name_game
        urls.append(urla)

    url = pd.DataFrame({
        'url': urls
    })

    return url


# if __name__ == '__main__':
#     data = pd.read_csv('datasets/final_dataset.csv')
#     data.platform = data.platform.apply(literal_eval)
#
#     result = get_data(data)
#     result.to_csv('datasets/urls_to_games.csv', index=False)
