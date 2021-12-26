from flask import Flask, render_template, request, redirect, url_for
from scraper_for_images import listUrls
import pandas as pd
from ast import literal_eval

pd.options.mode.chained_assignment = None

metadata = pd.read_csv('datasets/data_to_show_app.csv',
                       converters={'index': literal_eval, 'result': literal_eval, 'url_links': literal_eval,
                                   'score': literal_eval})
urls = pd.read_csv('datasets/urls.csv', converters={'urls': literal_eval}, index_col=0)
s = pd.Series(metadata.name_game)
app = Flask(__name__)


# Method returns list of links to images
def getUrls(indexes, urls):
    data = []
    for idx in indexes[0]:
        if len(urls.to_numpy()[idx, 0]) > 0:
            data.append(urls.to_numpy()[idx, 0][0])

    return data


# Main page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/error')
def bad_value():
    return render_template('error.html')


# Page with results
@app.route('/content', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST' or request.method == 'GET':
        user = request.form['search']

        if user in s.values:
            index = metadata[metadata.name_game == user].iloc[:, 0].to_list()
            links = getUrls(index, urls)
            game = metadata[metadata.name_game == user].iloc[:, 2].to_list()[0]
            link = metadata[metadata.name_game == user].iloc[:, 3].to_list()[0]
            score = metadata[metadata.name_game == user].iloc[:, 4].to_list()[0]
            return render_template('content.html', game=game, link=link, score=score, user=user, links=links)
        else:
            return render_template('error.html')


if __name__ == "__main__":
    app.run()
