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

System and testing for tagging loans with #JobCreator.
Caution: many loans identified that aren't tagged with #JobCreator are actually not tagged correctly.
Testing 1/31 success @ 100%
Despite passing tests, the system has not yet been deployed.
"""

import csv

from Other import auxilary

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
        if "labor" not in loan["use"] and "worker" not in loan["use"]:
            continue
        contains = False
        for tag in loan["tags"]:
            if tag["name"] == "#JobCreator":
                correct += 1
                contains = True
        if not contains:
            print("https://www.kiva.org/lend/" + str(loan["id"]), loan["use"])
        total += 1
        print(correct, total)