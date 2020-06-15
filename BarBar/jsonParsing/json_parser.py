import json
import os


def load_bars(file_path):
    print(os.getcwd())

    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)

    bars = data["bars"]

    return bars


def save(data):
    with open('bars_complete.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile)
