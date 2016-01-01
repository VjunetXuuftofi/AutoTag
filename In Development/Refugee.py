import requests
import json
import time
from datetime import datetime
from time import mktime
from datetime import timedelta



basetime = time.strptime("2015-12-20 18:10:04", "%Y-%m-%d %H:%M:%S")
basetime = datetime.fromtimestamp(mktime(basetime))


looking = ["IDP", "Internally Displaced Person", "internally displaced person"]

correct = 0
total = 0

ids = []

for match in looking:
    form = {
        "status" : "fundraising",
        "page" : "1",
        "app_id" : "com.woodside.autotag",
        "q": match
    }
    loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    loans = json.loads(loans)

    #specificity

    for i in range(1, int(loans["paging"]["pages"]+1)):
        page = str(i)
        form = {
            "status" : "fundraising",
            "page" : page,
            "app_id" : "com.woodside.autotag",
            "q" : match
        }
        loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
        loans = json.loads(loans)
        for a in loans["loans"]:
            postedtime = time.strptime(a["posted_date"], "%Y-%m-%dT%H:%M:%SZ")
            postedtime = datetime.fromtimestamp(mktime(postedtime))
            if basetime-postedtime >= timedelta(microseconds = 1):
                if a["id"] not in ids:
                    ids.append(a["id"])
                correctnow = correct
                for tag in a["tags"]:
                    for value in tag:
                        if tag[value] == "#Refugee":
                            correct += 1
                if correctnow == correct:
                    print(a["use"], a["id"])
                total += 1
print("Specificity: " + str(correct/total))

form = {
        "status" : "fundraising",
        "page" : "1",
        "app_id" : "com.woodside.autotag",
        "q": "#Refugee"
    }
total = 0
included = 0
loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
loans = json.loads(loans)
for i in range(1, int(loans["paging"]["pages"]+1)):
    page = str(i)
    form = {
        "status" : "fundraising",
        "page" : page,
        "app_id" : "com.woodside.autotag",
        "q" : "#Refugee"
    }
    loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    loans = json.loads(loans)
    for a in loans["loans"]:
        postedtime = time.strptime(a["posted_date"], "%Y-%m-%dT%H:%M:%SZ")
        postedtime = datetime.fromtimestamp(mktime(postedtime))
        if basetime-postedtime >= timedelta(microseconds = 1):
            if a["id"] in ids:
                included += 1
            else:
                print(a["id"], a["use"])
            total +=1
print("Sensitivity: " + str(included/total))



