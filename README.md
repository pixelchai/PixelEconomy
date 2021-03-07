# PixelEconomy

## Usage
Untested on any platforms apart from Arch Linux and Debian 10 (Google Cloud).

First install the following dependencies:
- Python3
- MongoDB

Then install the pip dependencies:
```
pip3 install -r requirements.txt
```

Start the MongoDB server:
```
cd mongo
sh start.sh
cd ..
```

Then run the project:
```
python3 app.py
```

Note: the above will only run a local development server locally on port 5050.
To serve a production server, use gunicorn:
```
gunicorn -b 0.0.0.0:80 app:app
```
