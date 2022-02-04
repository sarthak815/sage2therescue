import requests
import pandas as pd
import numpy as np
def getCoordinates(loc):
    try:
        API_KEY = "rlGYW7Wln1T4kVF97rdR7QCRvOIb-xVKrwrRFxlvA2w"
        resp = requests.get("https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey="+API_KEY+"&searchtext="+loc)
        respJson = resp.json()["Response"]
        viewJson = respJson["View"][0]
        result = viewJson["Result"][0]
        location = result["Location"]
        coordinates = location["DisplayPosition"]
        retVal = {"coordinates":coordinates, "status":1}
        return retVal
    except:
        return {"Error":"Error in finding location", "status":0}

def getCoordinates_df(df):
    try:
        coordinatesLatitude = []
        coordinatesLongitude = []
        for row in range(len(df)):
            loc = df.loc[row, "location"]
            try:
                coordinates = getCoordinates(loc)
                locCoord = coordinates['coordinates']
                coordinatesLatitude.append(locCoord['Latitude'])
                coordinatesLongitude.append(locCoord['Longitude'])
            except:
                coordinatesLatitude.append(np.nan)
                coordinatesLongitude.append(np.nan)
        df['Latitude'] = coordinatesLatitude
        df['Longitude'] = coordinatesLongitude
        return {'dataframe':df, 'status':1}
    except:
        return {"Error":"Error in finding location", "status":0}
# coordinates = getCoordinates("whitefield, bangalore")
# print(coordinates)
