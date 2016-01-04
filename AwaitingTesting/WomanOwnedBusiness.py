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

System and testing for tagging loans with #WomanOwnedBiz.
"""
import csv
from Other import auxilary

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))

loanids = ""
total = 0
everyloan = []
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
        borrowers = loan["borrowers"]
        description = loan["description"]["texts"]["en"]
        valid = True
        for borrower in borrowers:
            if borrower["gender"] == "M":
                valid = False
                break
        if not valid:
            continue
        if "husband" in description:
            # More than 85% of loans only to women without mention of "husband" have the tag, under 60% with "husband" do.
            continue
        if loan["activity"] in ["Personal Housing Expenses", "Farming", "Cattle", "Services", "Butcher Shop",
                                "Higher education costs", "Fishing", "Motorcycle Transport", "Property"]:
            continue
        if loan["sector"] in ["Health", "Personal Use", "Agriculture"]:
            continue
        partner = loan["partner_id"]
        for forbiddenpartner in ["BRAC Pakistan", "ID Ghana", "Hattha Kaksekar Limited (HKL), a partner of Save the Children",
                                "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                                "Hekima, a partner of World Relief",
                                "CAURIE Microfinance, a partner of Catholic Relief Services"]:
            if partner == auxilary.partnertoid(forbiddenpartner):
                valid = False
                break
        if not valid:
            continue
        contains = False
        for tag in loan["tags"]:
            if tag["name"] == "#WomanOwnedBiz":
                correct += 1
                contains = True
        if not contains:
            print(loan["id"])
        total += 1
        print(correct, total, loan)
print("Accuracy: " + str(correct/total))
