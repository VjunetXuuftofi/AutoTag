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
Testing 1/31 success @ 100%
This testing file is no longer necessary (the system has been deployed).
"""

import json
import csv
from Other import auxilary
import re

def tagElderly():
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


    correct = 0
    total = 0
    for loanlist in everyloan:
        for loan in loanlist:
            age = GetAge(loan["description"]["texts"]["en"])
            if age:
                if age < 50:
                    continue
            else:
                continue
            contains = False
            for tag in loan["tags"]:
                if tag["name"] == "#Elderly":
                    contains = True
                    correct += 1
                    break
            if not contains:
                print("https://www.kiva.org/lend/" + str(loan["id"]))
            total += 1
    print(correct, total)

def GetAge(description):
    match = re.findall(" ([1-9][1-9]) (years old|years of age|year old|year\-old)", description)
    if len(match) == 0:
        return None
    try:
        return int(match[0][0])
    except:
        return None
tagElderly()