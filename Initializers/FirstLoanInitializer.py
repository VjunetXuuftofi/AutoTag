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

Creates a csv relating loan uses to whether or not the loan should receive #WomanOwnedBiz. Then initializes and pickles
the vectorizer and randomforest objects for use in the bag of words approach.
"""

import csv
from Other import auxilary
from tqdm import tqdm
from Other import Analysis
import pickle
from bs4 import BeautifulSoup
import requests

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))


writer = csv.writer(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/FirstLoanBagOfWords.csv", "w+"))
writer.writerow(["id", "description", "value"])
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
        description = loan["description"]["texts"]["en"]
        if "repaid" in description:
            continue
        soup = BeautifulSoup(requests.get("https://www.kiva.org/lend/" + str(loan["id"])).text)
        if len(soup.find_all(id="prevLoanDetails")) != 0:
            continue
        contains = False
        for tag in loan["tags"]:
            if tag["name"] == "#FirstLoan":
                contains = True
                writer.writerow([loan["id"], description, 1])
        if not contains:
            writer.writerow([loan["id"], description, 0])
        print("done")

forest, vectorizer = Analysis.initialize("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/FirstLoanBagOfWords.csv")
pickle.dump(forest, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/FLForest", "wb+"))
pickle.dump(vectorizer, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/FLVectorizer", "wb+"))