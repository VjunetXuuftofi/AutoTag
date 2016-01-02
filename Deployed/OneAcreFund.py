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

System and testing for tagging loans from the partner One Acre Fund. Currently deployed.
"""

import json
import re
from Other import auxilary

def oafTag():
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

    loanlist = auxilary.getquery(form)

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

    for loans in loanlist:
        for loan in loans:
            loanid = str(loan["id"])
            auxilary.tag(loanid, "8")
            info = json.loads(auxilary.getinfo(loanid).text)
            description = info["loans"][0]["description"]["texts"]["en"]
            numborrowers = len(info["loans"][0]["borrowers"])
            try:
                pos = re.findall("a total of ([^ ]*?) solar lights.?", description)[0]
                if pos in conversions:
                    pos = conversions[pos]
                if int(pos) / int(numborrowers) > 0.5:
                    auxilary.tag(loanid, "9")
                    auxilary.tag(loanid, "38")
            except:
                pass
            vegan = True
            for forbidden in veganforbidden:
                if len(re.findall(" " + forbidden + "[^a-z]", description)) != 0:
                    vegan = False
                    break
            if vegan:
                auxilary.tag(loanid, "10")


