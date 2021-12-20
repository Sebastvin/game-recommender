from flask import Flask, render_template, request
import pandas as pd
from ast import literal_eval
pd.options.mode.chained_assignment = None

metadata = pd.read_csv('workpls.csv', converters={'index': literal_eval,'result': literal_eval, 'url_links': literal_eval,
                                                  'score': literal_eval})
s = pd.Series(metadata.name_game)
to_index = pd.read_csv('datasets/final_dataset.csv').loc[:, ['name_game']]

urls = pd.read_csv('urls.csv', converters={'urls': literal_eval}, index_col=0)


app = Flask(__name__)


def toUrls(indexes, urls):
    data = []
    for idx in indexes[0]:
        if len(urls.to_numpy()[idx, 0]) > 0:
            data.append(urls.to_numpy()[idx, 0][0])

    return data



@app.route('/')
def home():
    return (render_template('index.html'))


@app.route('/content',  methods=['GET', 'POST'])
def get_data():
    def toUrls(indexes, urls):
        data = []
        for idx in indexes[0]:
            if len(urls.to_numpy()[idx, 0]) > 0:
                data.append(urls.to_numpy()[idx, 0][0])

        return data

    if request.method == 'POST' or request.method == 'GET':
        user = request.form['search']

        if user in s.values:
            index = metadata[metadata.name_game == user].iloc[:, 0].to_list()
            links = toUrls(index, urls)
            game = metadata[metadata.name_game == user].iloc[:, 2].to_list()[0]
            link = metadata[metadata.name_game == user].iloc[:, 3].to_list()[0]
            score = metadata[metadata.name_game == user].iloc[:, 4].to_list()[0]
            return render_template('content.html', game=game, link=link, score=score, user=user, links=links)
        else:
            return render_template('index.html')


if __name__ == "__main__":
    app.run()