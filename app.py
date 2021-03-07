from datetime import datetime
import flask_login
from db import db
from logger import logger
import json

import flask
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
app.secret_key = "PixelEconomy"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

def check_credentials(username, password):
    return db["users"].find_one({"username": username, "password": password})

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if check_credentials(request.form.get('username'), request.form.get('password')):
        user = User()
        user.id = username
        user.is_authenticated = True

        return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template("pages/login.html", title="Login", nosidebar=True)

    username = flask.request.form['username']
    password = flask.request.form['password']
    if check_credentials(username, password):
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("index"))
    return render_template("msg-redir.html", nosidebar=True, content="Bad login")


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template("msg-redir.html", nosidebar=True, content="Logged out")

@app.context_processor
def inject_site_data():
    return {
        "site": {
            "title": "PixelEconomy",
            "tagline": "Virtual marketplace for pixel art",
            # "url": "",
            "version": "0.1.0",
            # "google_analytics_id": "",
            "year": datetime.now().year,
        }
    }

@app.context_processor
def inject_user_data():
    try:
        user_data = db["users"].find_one({"username": flask_login.current_user.id})
        return {
            "user": {
                "username": user_data["username"],
                "balance": user_data["balance"],
            }
        }
    except:
        return {
            "user": {
                "username": "invalid",
                "balance": -1,
            }
        }


@app.route('/res/<path:path>')
def send_res(path):
    return send_from_directory('res', path)


@app.route('/marketplace')
@flask_login.login_required
def marketplace():
    arts = []

    # get arts from database
    for market_entry in db["market"].find():
        art_id = market_entry["art"]

        data_art = db["art"].find_one({"_id": art_id})
        creator_username = db["users"].find_one({"_id": data_art["creator"]})["username"]
        arts.append({
            "title": data_art["title"],
            "creator": creator_username,
            "price": market_entry["price"],
            "data": data_art["data"],
        })

    return render_template(r"pages/marketplace.html", title="Marketplace", arts=arts)

@app.route('/my-portfolio')
@flask_login.login_required
def my_portfolio():
    arts = []

    # get arts from database
    try:
        user_data = db["users"].find_one({"username": flask_login.current_user.id})
        for art_id in user_data["portfolio"]:
            data_art = db["art"].find_one({"_id": art_id})
            creator_username = db["users"].find_one({"_id": data_art["creator"]})["username"]
            arts.append({
                "title": data_art["title"],
                "creator": creator_username,
                "data": data_art["data"],
            })
    except:
        pass

    return render_template(r"pages/my-portfolio.html", title="My Portfolio", arts=arts)


@app.route('/create')
@flask_login.login_required
def create():
    return render_template(r"pages/create.html", title="Create")

@app.route("/about")
@flask_login.login_required
def about():
    return render_template(r"pages/about.html", title="About")

@app.route("/")
def index():
    logged_in = False
    try:
        logger.debug("Logged in visit to index: {}".format(flask_login.current_user.id))
        logged_in = True
    except:
        pass

    if logged_in:
        return flask.redirect(flask.url_for("marketplace"))
    else:
        return flask.redirect(flask.url_for("login"))

@app.route("/api/save", methods=['POST'])
def api_save():
    body = json.loads(flask.request.data.decode('utf8'))
    try:
        user_data = db["users"].find_one({"username": flask_login.current_user.id})
        art_id = db["art"].insert_one({
            "title": body["title"],
            "creator": user_data["_id"],
            "data": body["data"]
        }).inserted_id
        db["users"].update_one({"_id": user_data["_id"]}, {"$push": {"portfolio": art_id}})
    except:
        pass

    return ""



if __name__ == '__main__':
    app.run()
