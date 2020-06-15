import json
import os

def loadBars(filePath):

    print(os.getcwd())

    with open(filePath, 'r', encoding='utf8') as f:
        data = json.load(f)

    bars = data["bars"]

    return bars

def save(data):

    with open('barsComplete.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile)