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
import json

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
        if loan["activity"] in ["Personal Medical Expenses", "Rickshaw", "Home Appliances",
                         "Wedding Expenses", "Consumer Goods", "Electrical Goods",
                         "Vehicle", "Auto Repair", "Electronics Sales", "Higher education costs",
                         "Laundry", "Spare Parts", "Vehicle Repairs",
                         "Taxi",
                         "Health",
                         "Farm Supplies", "Personal Purchases", "Transportation", "Fishing", "Mobile Phones",
                         "Cattle", "Farming",
                         "Butcher Shop", "Milk Sales",
                         "Motorcycle Transport", "Animal Sales", "Home Energy", "Used Shoes", "Hardware", "Property",
                         "Bakery", "Dairy", "Poultry", "Agriculture", "Clothing", "Livestock"]:
            print("Activity")
            continue
        partner = loan["partner_id"]
        if partner == 415: #Partners in Health
            continue
        if partner == 120: #ADIM
            continue
        if partner == 58: #Fundacion Paraguaya
            continue
        for forbiddenpartner in ["Habitat for Humanity Mexico", "VisionFund Cambodia", "Alivio Capital",
                         "Hattha Kaksekar Limited (HKL), a partner of Save the Children", "Kenya ECLOF", "One Acre Fund",
                         "Entrepreneurs du Monde - Anh Chi Em", "SEF International", "BRAC Pakistan", "MDO Humo and Partners",
                         "VisionFund Albania", "Bai Tushum Bank CJSC", "Hekima, a partner of World Relief",
                         "M7 Microfinance Institution Limited",
                         "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                        "CIDRE", "Kashf Foundation", "ID Ghana", "Ibdaa Microfinance SAL",
                         "Paglaum Multi-Purpose Cooperative (PMPC)", "CAURIE Microfinance, a partner of Catholic Relief Services"]:
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
