import logging.config
import os
import pathlib
import json
from app import north_wind_app

def setup_logging():
    config_file = pathlib.Path(os.path.join("config", "logging_config.json"))
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)



if __name__ == "__main__":
    setup_logging()
    north_wind_app.run(debug=True)

