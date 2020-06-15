import jsonParser as parser
from geopy.geocoders import Nominatim
import sys

locator = Nominatim(user_agent="myGeocoder")

file = "jsonParsing/bars.json"
bars = parser.loadBars(file)
numberBars = len(bars)

toRemove = []
i = 0
for bar in bars:

    i = i + 1
    sys.stdout.write("Getting adress number %d out of %d \r" % (i, numberBars))
    sys.stdout.flush()

    address = bar["address"]
    location = locator.geocode(address)

    if location:
        bar["latitude"] = location.latitude
        bar["longitude"] = location.longitude
    else:
        print("could not locate bar %s" % address)
        toRemove.append(bar)

localizedBars = [bar for bar in bars if bar not in toRemove]

json = {
    "bars" : localizedBars
}

parser.save(json)