import json
import os

from src.utils import load_env

load_env()


def read_json():
    with open(os.environ["CONFIG_PATH"], "r") as f:
        return json.load(f)


config = read_json()
