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

Initializes machine learning tools for tagging #JobCreator.
"""

import csv
import pickle
from Other import Analysis

writer = csv.writer(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/"
    "JCBagOfWords.csv",
    "w+"))
writer.writerow(["id", "description", "value"])
ids = []
loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions.csv"))
for loan in loans:
    if "#JobCreator" in loan["Tags"]:
        writer.writerow([loan["Loan ID"], loan["Use"], 1])
    else:
        writer.writerow([loan["Loan ID"], loan["Use"], 0])

forest, vectorizer, selector = Analysis.initialize("JC")
pickle.dump(forest, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/JCForest",
    "wb+"))
pickle.dump(vectorizer, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "JCVectorizer",
    "wb+"))
pickle.dump(selector, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "JCSelector",
    "wb+"))
