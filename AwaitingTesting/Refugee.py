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

System and testing for tagging loans with #Refugee.
"""

import csv
import re
from Other import auxilary
import json


looking = ["IDP", "Internally Displaced Person", "internally displaced person", "Refugee", "refugee"]


ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))


loanids = ""

everyloan = []
total = 0
for loan in loans:
    loanids += loan["Loan ID"] + ","
    total += 1
    if total == 100:
        total = 0
        loanids = loanids[:-1]
        loanlist = auxilary.getinfo(loanids)
        loanids = ""
        everyloan.append(loanlist)

total = 0
correct = 0
for loangroup in everyloan:
    for loan in loangroup:
        use = loan["use"]
        description = loan["description"]["texts"]["en"]
        escape = True
        for match in looking:
            if len(re.findall(" " + match + "[^A-z]", description)) > 0:
                escape = False
                break
        if escape:
            continue
        if "Gaza Strip" in description:
            continue
        contains = False
        for tag in loan["tags"]:
            if tag["name"] == "#Refugee":
                correct += 1
                contains = True
        if not contains:
            print(loan["id"])
        total += 1
        print(correct, total)