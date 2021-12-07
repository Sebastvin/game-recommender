from flask import Flask, render_template, request, redirect, url_for
from recommendation_system import  get_recommendations
from scraper_for_images import listUrls
import pandas as pd
pd.options.mode.chained_assignment = None


app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return (render_template('index.html'))


@app.route('/content',  methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST' or request.method == 'GET':
        user = request.form['search']
        game = get_recommendations(str(user))
        #urlsImg = listUrls(game.iloc[:, 0].values)
        des = game.iloc[:, 1].values
        score = game.iloc[:, 2].tolist()
        link = game.iloc[:, 6].tolist()
        print(link)
        root = "Recommendations for "
        return render_template('content.html', game=des, name= root + str(user), des=des, urlsImg=des, score=score,
                               link=link)


if __name__ == "__main__":
    app.run(debug=True)