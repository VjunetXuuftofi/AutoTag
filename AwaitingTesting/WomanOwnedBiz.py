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

System and testing for tagging loans with #FemaleEducation.
Testing 1/31 failed @ 75%
"""

import csv
import re
from Other import auxilary
import json
from tqdm import tqdm
from Other import Analysis



ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))

forest, vectorizer = Analysis.initialize("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/WomanOwnedBizBagOfWords.csv")
loanstowrite = []
loanids = ""

everyloan = []
total = 0
for loan in tqdm(loans):
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
        valid = True
        for borrower in loan["borrowers"]:
            if borrower["gender"] == "M":
                valid = False
                break
        if not valid:
            continue
        '''
        if loan["activity"] in ["Personal Housing Expenses", "Farming", "Cattle", "Services", "Butcher Shop",
                                "Higher education costs", "Fishing", "Motorcycle Transport", "Property"]:
            continue
        if loan["sector"] in ["Health", "Personal Use", "Agriculture"]:
            continue
        partner = loan["partner_id"]
        for forbiddenpartner in ["BRAC Pakistan", "ID Ghana", "Hattha Kaksekar Limited (HKL), a partner of Save the Children",
                                "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                                "Hekima, a partner of World Relief",
                                "CAURIE Microfinance, a partner of Catholic Relief Services", "Kashf Foundation"]:
            if partner == auxilary.partnertoid(forbiddenpartner):
                valid = False
                break
        if not valid:
            continue
            '''
        description = loan["description"]["texts"]["en"]
        modified = [Analysis.modify(description)]
        if modified != [None]:
            modified = vectorizer.transform(modified).toarray()
            prediction = forest.predict_proba(modified)
            if prediction[0][0] > 0.01:
                continue
        else:
            continue

        contains = False
        for tag in loan["tags"]:
            if tag["name"] == "#WomanOwnedBiz":
                contains = True
                correct += 1
        if not contains:
            print("http://www.kiva.org/lend/" + loan["id"])
        total +=1
        print(correct, total)