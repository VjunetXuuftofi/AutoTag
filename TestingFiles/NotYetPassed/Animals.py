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

System for testing machine learning tools for #Animals.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = ["http://kiva.org/lend/1014200", "http://kiva.org/lend/1011267",
       "http://kiva.org/lend/1010561",
       "http://kiva.org/lend/1010636", "http://kiva.org/lend/1008725",
       "http://kiva.org/lend/999036",
       "http://kiva.org/lend/997683", "http://kiva.org/lend/999139",
       "http://kiva.org/lend/994646",
       "http://kiva.org/lend/992451", "http://kiva.org/lend/990434",
       "http://kiva.org/lend/990318",
       "http://kiva.org/lend/987598", "http://kiva.org/lend/1026756",
       "http://kiva.org/lend/1029128",
       "http://kiva.org/lend/1029069", "http://kiva.org/lend/1017299",
       'http://kiva.org/lend/1042634',
       'http://kiva.org/lend/1041690', 'http://kiva.org/lend/1043861',
       'http://kiva.org/lend/1042909',
       'http://kiva.org/lend/1041011', 'http://kiva.org/lend/1042633',
       'http://kiva.org/lend/1035240',
       'http://kiva.org/lend/1045090', 'http://kiva.org/lend/1041987',
       'http://kiva.org/lend/1010492', 'http://kiva.org/lend/1014295',
       'http://kiva.org/lend/1011156',
       'http://kiva.org/lend/1007157', 'http://kiva.org/lend/1024575']

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/AForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "AVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "ASelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2featuresUse",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if loan["Activity"] == "Butcher Shop" or loan[
        "Activity"] == "Food Market" \
            or loan["Activity"] == "Veterinary Sales" \
            or loan["Activity"] == "General Store":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .6:
            continue
        print(prediction[0][1])
    else:
        continue
    if "#Animals" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
