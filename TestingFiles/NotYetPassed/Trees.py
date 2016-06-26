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

System for testing machine learning tools for #Trees.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = ['http://kiva.org/lend/1042898', 'http://kiva.org/lend/1045121',
       'http://kiva.org/lend/1035908']

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined3.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/TrForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "TrVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "TrSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined3featuresUse",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if loan["Partner Name"] == "One Acre Fund":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .5:
            continue
        print(prediction[0][1])
    else:
        continue
    if "#Trees" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
