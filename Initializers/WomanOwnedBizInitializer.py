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

Creates a csv relating loan descriptions to whether or not the loan should receive #WomanOwnedBiz. Then feeds this data to
the initializer in Analysis.py and saves the results to pickle files.
"""

import csv
from Other import Analysis
import pickle

writer = csv.writer(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/WOBBagOfWords.csv", "w+"))
writer.writerow(["id", "description", "value"])
ids = []
loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions.csv"))
for loan in loans:
    if loan["Women"] == 0:
        continue
    if loan["Partner Name"] == "Emprender" or loan["Partner Name"] == "Paglaum Multi-Purpose Cooperative (PMPC)" \
            or loan["Partner Name"] == "Interactuar" \
            or loan["Partner Name"] == "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International"\
            or loan["Partner Name"] == "Apoyo Integral"\
            or loan["Partner Name"] == "Thanh Hoa Microfinance Institution Limited Liability"\
            or loan["Partner Name"] == "Vision Finance Company s.a. (VFC), a partner of World Vision International"\
            or "Pro Mujer" in loan["Partner Name"]:
        continue
    if loan["Activity"] == "Personal Medical Expenses" or loan["Sector"] == "Personal Use" or loan["Sector"] == "Education"\
            or loan["Activity"] == "Personal Housing Expenses":
        continue
    if "#WomanOwnedBiz" in loan["Tags"]:
        writer.writerow([loan["Loan ID"], loan["Description"], 1])
    else:
        writer.writerow([loan["Loan ID"], loan["Description"], 0])

forest, vectorizer, selector = Analysis.initialize("WOB", [250, 2])
pickle.dump(forest, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/WOBForest", "wb+"))
pickle.dump(vectorizer, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/WOBVectorizer", "wb+"))
pickle.dump(selector, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/WOBSelector", "wb+"))
