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

System and testing for tagging loans with #Elderly, as well as detecting the age of borrowers.
"""

import json
import csv
from Other import auxilary
import re

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
for loan in loans:
    info = json.loads(auxilary.getinfo(loan["Loan ID"]).text)
    description = info["loans"][0]["description"]["texts"]["en"]
    match = re.findall(" ([1-9][1-9]) (years old|years of age|year old|year\-old)", description)
    if len(match) == 0:
        continue
    try:
        if int(match[0][0]) < 50:
            continue
    except:
        continue
    if loan["Tags"] == "":
        continue
    if "#Elderly" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Raw Link"])
    total += 1
    print(correct, total, match)