import requests
import json
import re
import time
import auxilary

form = {
    "status" : "fundraising",
    "partner" : "202",
    "page" : "1",
    "app_id" : "com.woodside.autotag"
}

veganforbidden = ["goat", "dairy", "cow", "calf", "calves", "chicken", "chicks", "buffalo", "rabbit", "sheep", "duck", "pig",
           "duckling", "lamb", "cattle", "bull", "ram", "poultry", "honey", "bee", "animal", "livestock",
           "ox", "steer", "heifer", "turkey", "hen", "piglet",
           "goats", "cows", "chickens", "chicks", "buffalos", "rabbits", "ducks", "pigs", "ducklings", "lambs",
           "bulls", "rams", "bees", "animals", "oxen", "steers", "heifers", "turkeys", "sows", "hens", "piglets"]

loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
loans = json.loads(loans)

conversions = {
    "one" : "1",
    "two" : "2",
    "three" : "3",
    "four" : "4",
    "five" : "5",
    "six" : "6",
    "seven" : "7",
    "eight" : "8",
    "nine" : "9",
    "ten" : "10",
    "eleven" : "11",
    "twelve" : "12",
    "thirteen" : "13",
    "fourteen" : "14",
    "fifteen" : "15",
    "sixteen" : "16",
    "seventeen" : "17",
    "eighteen" : "18",
    "nineteen" : "19"
}

for i in range(1, int(loans["paging"]["pages"])):
    page = str(i)
    form = {
    "status" : "fundraising",
    "partner" : "202",
    "page" : page,
    "app_id" : "com.woodside.autotag"
    }
    loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    loans = json.loads(loans)
    for a in loans["loans"]:
        loanid = str(a["id"])
        print(loanid)
        form = {
            "checked" : "true",
            "tag_id" : "8",
            "business_id" : loanid,
            "user_id" : "1442043"
            }
        heads = {
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Connection" : "keep-alive",
            "DNT" : "1",
            "Host" : "www.kiva.org",
            "Referer" : "http://www.kiva.org/lend/" + loanid,
            "Accept-Encoding" : "gzip, deflate",
            "Accept-Language" : "en-US,en;q=0.8",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36"
        }
        requests.post("https://www.kiva.org/ajax/addOrRemoveLoanTag?",
                    headers = heads,
                    data = form
                    )
        info = json.loads(auxilary.getinfo(loanid).text)
        description = info["loans"][0]["description"]["texts"]["en"]
        numborrowers = len(info["loans"][0]["borrowers"])
        try:
            pos = re.findall("a total of ([^ ]*?) solar lights.?", description)[0]
            if pos in conversions:
                pos = conversions[pos]
            if int(pos) / int(numborrowers) > 0.5:
                form["tag_id"] = "9"
                requests.post("https://www.kiva.org/ajax/addOrRemoveLoanTag?",
                headers = heads,
                data = form)
                form["tag_id"] = "38"
                requests.post("https://www.kiva.org/ajax/addOrRemoveLoanTag?",
                headers = heads,
                data = form)
        except:
            pass
        vegan = True
        for forbidden in veganforbidden:
            if len(re.findall(" " + forbidden + "[^a-z]", description)) != 0:
                vegan = False
                break
        if vegan:
            form["tag_id"] = "10"
            form["checked"] = "false"
            requests.post("https://www.kiva.org/ajax/addOrRemoveLoanTag?",
                    headers = heads,
                    data = form)


