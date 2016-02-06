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

def oafTag(everyloan):


    #veganforbidden = ["goat", "dairy", "cow", "calf", "calves", "chicken", "chicks", "buffalo", "rabbit", "sheep", "duck", "pig",
    #           "duckling", "lamb", "cattle", "bull", "ram", "poultry", "honey", "bee", "animal", "livestock",
    #           "ox", "steer", "heifer", "turkey", "hen", "piglet",
    #          "goats", "cows", "chickens", "chicks", "buffalos", "rabbits", "ducks", "pigs", "ducklings", "lambs",
    #           "bulls", "rams", "bees", "animals", "oxen", "steers", "heifers", "turkeys", "sows", "hens", "piglets"]



    for loanlist in everyloan:
        for loan in loanlist:
            loanid = str(loan["id"])
            auxilary.tag(loanid, "8")
            auxilary.tag(loanid, "9")
            description = loan["description"]["texts"]["en"]
            numborrowers = len(loan["borrowers"])
            try:
                pos = re.findall("a total of ([^ ]*?) solar lights.?", description)[0]
                if pos in conversions:
                    pos = conversions[pos]
                if int(pos) > 0.5 * numborrowers:
                    auxilary.tag(loanid, "38")
            except:
                pass
            '''
            vegan = True
            for forbidden in veganforbidden:
                if len(re.findall(" " + forbidden + "[^a-z]", description)) != 0:
                    vegan = False
                    break
            if vegan:
                auxilary.tag(loanid, "10")
                '''


