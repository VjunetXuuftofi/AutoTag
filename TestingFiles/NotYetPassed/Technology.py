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

System for testing machine learning tools for tagging #Technology.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = []

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined3.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/TForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "TVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "TSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined3featuresUse",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if (loan["Partner Name"] == "One Acre Fund" and "solar light" in loan[
        "Description"]) \
            or loan["Partner Name"] in ["PT Rekan Usaha Mikro Anda (Ruma)",
                                        "African Clean Energy(ACE)",
                                        "iSmart Kenya"] \
            or (loan["Partner Name"] in ["iDE Cambodia",
                                         "TerraClear Development"] and
                "water filter" in loan["Use"]) or "solar" in loan["Use"]:
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
    if "#Technology" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
