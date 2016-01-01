import requests
import json
import time

def explorer(FP):
    tags = {}

    total = 0

    form = {
        "partner" : FP,
        "page" : "1",
        "app_id" : "com.woodside.autotag"
    }
    loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    loans = json.loads(loans)
    for i in range(1, int(loans["paging"]["pages"])):
        page = str(i)
        form = {
        "partner" : FP,
        "page" : page,
        "app_id" : "com.woodside.autotag"
        }
        response = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form)
        loans = json.loads(response.text)
        headers = response.headers
        time.sleep(60/(int(headers["X-RateLimit-Overall-Limit"])))
        for loan in loans["loans"]:
            total += 1
            if len(loan["tags"]) > 0:
                for tag in loan["tags"]:
                    tag = tag["name"]
                    if tag != "volunteer_pick" and tag != "volunteer_like" and tag != "user_favorite":
                        try:
                            tags[tag] += 1
                        except:
                            tags[tag] = 1
    return tags, total

