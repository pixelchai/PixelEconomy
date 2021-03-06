from datetime import datetime
import flask_login
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):
    pass

@app.context_processor
def inject_site_data():
    return {
        "site":{
            "title": "PixelEconomy",
            "tagline": "Virtual marketplace for pixel art",
            # "url": "",
            "version": "0.1.0",
            # "google_analytics_id": "",
            "year": datetime.now().year,
        }
    }

@app.route('/res/<path:path>')
def send_res(path):
    return send_from_directory('res', path)

@app.route('/')
def marketplace():
    return render_template(r"pages/marketplace.html", title="Marketplace")

@app.route('/create')
def create():
    return render_template(r"pages/create.html", title="Create")


if __name__ == '__main__':
    app.run()
