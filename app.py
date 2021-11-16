from flask import Flask, render_template, request, redirect, url_for
from recommendation_system import  get_recommendations


app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return (render_template('index.html'))


@app.route('/content',  methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST' or request.method == 'GET':
        user = request.form['search']
        game = get_recommendations(str(user)).values
        root = "Recommendations for "
        return render_template('content.html', test=game, name= root + str(user))


if __name__ == "__main__":
    app.run(debug=True)