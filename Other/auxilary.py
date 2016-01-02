"""
Copyright 2016 Thomas Woodside

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Some helpful functions to be used in almost every tagging system.
"""

import requests
import json
import time



def getinfo(ID):
    """Pulls data about a specific loan from the Kiva API.
    Includes a time sleep to ensure that usage limits aren't exceeded."""
    ID = str(ID)
    response = requests.get("http://api.kivaws.org/v1/loans/" + ID + ".json",
                 params = {"ids" : ID, "appid" : "com.woodside.autotag"})
    headers = response.headers
    time.sleep(60/(int(headers["X-RateLimit-Overall-Limit"])-5))
    return response


def explorer(FP):
    """Returns the tag breakdown of a Field Partner"""
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

def tag(loanID, tagID):
    """Tags a loan with the desired tag."""
    form = {
                "checked" : "true",
                "tag_id" : tagID,
                "business_id" : loanID,
                "user_id" : "1442043"
                }
    heads = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        "Connection" : "keep-alive",
        "DNT" : "1",
        "Host" : "www.kiva.org",
        "Referer" : "http://www.kiva.org/lend/" + loanID,
        "Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "en-US,en;q=0.8",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36"
    }
    requests.post("https://www.kiva.org/ajax/addOrRemoveLoanTag?",
                headers = heads,
                data = form
                )


def getquery(form):
    toreturn = []
    info = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    info = json.loads(info)
    for i in range(1, int(info["paging"]["pages"])):
        form["page"] = str(i)
        loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
        loans = json.loads(loans)["loans"]
        toreturn.append(loans)
    return toreturn
