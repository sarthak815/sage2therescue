import requests

def getCoordinates(loc):
    try:
        API_KEY = "i5FirvKqWok47Llil731Lhun0hUgjnyit124TzkE5hM"
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

# coordinates = getCoordinates("whitefield, bangalore")
# print(coordinates)
