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

Runs all of the implemented systems
"""
from Other import auxilary
from Deployed import OneAcreFund
import time
from datetime import timedelta
from datetime import datetime
from pync import Notifier

while True:
    lasttried = open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/time.txt", "r")
    for line in lasttried:
        lasttime = datetime.fromtimestamp(time.mktime(time.strptime(line, "%d %b %Y %H:%M:%S")))
    lasttried.close()
    form = {
            "status": "fundraising",
            "partner": "202",
            "page": "1",
            "app_id": "com.woodside.autotag"
        }

    loanlist = auxilary.getquery(form)
    loanids = ""
    total = 0
    everyloan = []
    timetowrite = lasttime

    for loans in loanlist:
        for loan in loans:
            postedtime = datetime.fromtimestamp(time.mktime(time.strptime(loan["posted_date"], "%Y-%m-%dT%H:%M:%SZ")))
            if postedtime - timetowrite > timedelta(microseconds = 1):
                timetowrite = postedtime
            if lasttime - postedtime > timedelta(microseconds = 1):
                continue
            loanids += str(loan["id"]) + ","
            total += 1
            if total == 100:
                total = 0
                loanids = loanids[:-1]
                everyloan.append(auxilary.getinfo(loanids))
                loanids = ""
    everyloan.append(auxilary.getinfo(loanids[:-1]))
    OneAcreFund.oafTag(everyloan)
    lasttried = open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/time.txt", "w+")
    lasttried.write(time.strftime("%d %b %Y %H:%M:%S", timetowrite.timetuple()))
    lasttried.close()
    Notifier.notify("Tagging Complete.")
    time.sleep(86400)
