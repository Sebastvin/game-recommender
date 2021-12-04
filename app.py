import flask

app = flask.Flask(__name__, template_folder='templates')


# Set up the main route

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
