import requests
import time
def getinfo(ID):
    ID = str(ID)
    response = requests.get("http://api.kivaws.org/v1/loans/" + ID + ".json",
                 params = {"ids" : ID, "appid" : "com.woodside.autotag"})
    headers = response.headers
    time.sleep(60/(int(headers["X-RateLimit-Overall-Limit"])-5))
    return response