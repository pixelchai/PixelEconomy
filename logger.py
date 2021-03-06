import logging
import os
import sys

# Setup logging
logger = logging.getLogger("PixelEconomy")

def init_logger():
    os.makedirs("log", exist_ok=True)

    log_filename = os.path.join("log", "pixeleconomy.log")

    fh = logging.FileHandler(filename=log_filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s (%(module)s %(pathname)s:%(lineno)s) - %(levelname)s - %(message)s"
        )
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) <= 0:
        logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("logger init! "+str("-"*200))

init_logger()