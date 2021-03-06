from logger import logger
import pymongo
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["pixeleconomy"]

mock_db = {
    "users": {
        "bobJoss": {
            "palettes": ["Basic", "Greyscale", "Gameboy-like"],
            "balance": 500,
            "password": "hello123",  # very insecure, needs improving before prod
            "portfolio": [
                1234,
            ]
        }
    },
    "art": {
        1234: {
            "title": "Abstract Art",
            "creator": "badArtist",
            # owner get by querying users
            "data": "data:image/png;base64,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",
        }
    },
    "palettes": {
        "Basic": {
            "colours": [
                "#FFFFFF",
                "#000000"
            ],
            "price": 0,
        },
        "Greyscale": {
            "colours": [
                "#DDDDDD",
                "#AAAAAA",
                "#777777",
                "#555555",
                "#222222"
            ],
            "price": 0
        },
        "Gameboy-like": {
            "colours": [
                "#F9FFB3",
                "#ABCC47",
                "#3D8026",
                "#1B2E3A",
                "#00131A"
            ],
            "price": 0
        },
    },
    "market": [
        1234,
    ]
}


def init():
    if db["db_meta"].find_one({"initialised": True}):
        logger.info("Database has already been initialised!")
        return

    db["palettes"].insert_many([
        {
            "name": "Basic",
            "colours": [
                "#FFFFFF",
                "#000000"
            ],
            "price": 0,
        },
        {
            "name": "Greyscale",
            "colours": [
                "#DDDDDD",
                "#AAAAAA",
                "#777777",
                "#555555",
                "#222222"
            ],
            "price": 0
        },
        {
            "name": "Gameboy-like",
            "colours": [
                "#F9FFB3",
                "#ABCC47",
                "#3D8026",
                "#1B2E3A",
                "#00131A"
            ],
            "price": 0
        }
    ])
    logger.debug("Initialised palettes")

    # update initialised status
    db["db_meta"].insert_one({
        "initialised": True,
    })
    logger.info("Initialised database!")


init()
# db["db_meta"].drop()
