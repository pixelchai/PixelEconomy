from flask import Flask

app = Flask(__name__)


@app.route('/')
def marketplace():
    return 'Hello World!'

@app.context_processor
def inject_globals():
    return {
        "title": "PixelEconomy",
        "tagline": "Virtual marketplace for pixel art",
        # "url": "",
        "version": "0.1.0",
        # "google_analytics_id": "",
    }


if __name__ == '__main__':
    app.run()
