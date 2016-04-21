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

System for testing machine learning tools for #Refugee.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = ['http://kiva.org/lend/1036651', 'http://kiva.org/lend/1036653',
       'http://kiva.org/lend/1034941', 'http://kiva.org/lend/998192'
       ]

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/RForest",
    "rb"))
print(forest.best_params_)
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "RVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "RSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2"
    "featuresDescription",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
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
    if "#Refugee" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
