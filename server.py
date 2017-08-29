from flask import (Flask,render_template)

from db.models_data import Tweet, Branch, calldb

app = Flask(__name__, static_url_path='/static', static_folder='static')

db = calldb()

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/manuel")
def manuel():
    q = Tweet.select().where(Tweet.branch==3).order_by(Tweet.tweet_id)[:100]
    return render_template('lista.html', tweets=q)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run('0.0.0.0', 8000, threaded=True, debug=False)
