from math import ceil

from flask import (Flask,render_template)

from db.models_data import Tweet, Branch, calldb

app = Flask(__name__, static_url_path='/static', static_folder='static')

db = calldb()

@app.route("/about")
def hello():
    return render_template('about.html')

@app.route("/manuel")
@app.route("/manuel/<int:page>")
def manuel(page=1):
    per_page = 40
    query = Tweet.select().where(Tweet.branch==4).order_by(Tweet.tweet_id)
    pages = int(ceil(float(query.count()) / per_page))

    result = query.paginate(page, per_page)
    return render_template('lista.html', tweets=result, page=page, pages=pages)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run('0.0.0.0', 8000, threaded=True, debug=False)
