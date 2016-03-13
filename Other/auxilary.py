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

Two useful methods to pull data from the Kiva API.
"""

import requests
import json
import time
from collections import defaultdict
import re
from tqdm import tqdm
from datetime import timedelta
from datetime import datetime


def getinfo(IDs):
    """
    Pulls and returns data about specific loans from the Kiva API.
    Includes a time sleep to ensure that usage limits aren't exceeded.
    No more than 100 loan ID
    :param IDs:
    :return loans:
    """
    response = requests.get("http://api.kivaws.org/v1/loans/" + IDs + ".json",
                 params = {"appid" : "com.woodside.autotag"})
    time.sleep(60/55)
    loans = json.loads(response.text)["loans"]
    return loans

def getquery(form, lasttime = None):
    """
    Takes in an HTTP form and submits this form with the Kiva API. All data from the form is returned as a list of
    dictionaries. Optionally, a datetime object can be included to stop getting more information once that data is older
    than the query.
    :param form:
    :param lasttime:
    :return queryresults:
    """
    queryresults = []
    info = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    info = json.loads(info)
    for i in range(1, int(info["paging"]["pages"])):
        form["page"] = str(i)
        response = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form)
        time.sleep(60/55)
        loans = json.loads(response.text)["loans"]
        queryresults.append(loans)
        if (lasttime):
            out = False
            for loan in loans:
                postedtime = datetime.fromtimestamp(time.mktime(time.strptime(loan["posted_date"], "%Y-%m-%dT%H:%M:%SZ")))
                if lasttime - postedtime > timedelta(microseconds = 1):
                    out = True
                    break
            if out:
                break
    return queryresults