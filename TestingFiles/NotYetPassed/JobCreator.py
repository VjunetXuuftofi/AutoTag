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

System for testing machine learning tools for #IncomeProducingDurableAsset
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = [
    'http://kiva.org/lend/1004055', 'http://kiva.org/lend/1018838',
       'http://kiva.org/lend/997325', 'http://kiva.org/lend/992609',
       'http://kiva.org/lend/1006253', 'http://kiva.org/lend/1019313',
       'http://kiva.org/lend/992461', 'http://kiva.org/lend/998365',
       'http://kiva.org/lend/991594', 'http://kiva.org/lend/1009874',
       'http://kiva.org/lend/991695', 'http://kiva.org/lend/1010336',
       'http://kiva.org/lend/1001517', 'http://kiva.org/lend/1006342',
       'http://kiva.org/lend/997936', 'http://kiva.org/lend/1010150',
       'http://kiva.org/lend/991797', 'http://kiva.org/lend/1019255',
       'http://kiva.org/lend/997315', 'http://kiva.org/lend/1003956',
       'http://kiva.org/lend/1018720', 'http://kiva.org/lend/1010566',
    'http://kiva.org/lend/994958', 'http://kiva.org/lend/1019968',
    'http://kiva.org/lend/1021984', 'http://kiva.org/lend/988961',
    'http://kiva.org/lend/1009713', 'http://kiva.org/lend/1023645',
    'http://kiva.org/lend/1008606', 'http://kiva.org/lend/1025616',
    'http://kiva.org/lend/1010371', 'http://kiva.org/lend/1024063',
    'http://kiva.org/lend/1021881', 'http://kiva.org/lend/1000399',
    'http://kiva.org/lend/1022029', 'http://kiva.org/lend/1009643',
    'http://kiva.org/lend/991177', 'http://kiva.org/lend/988255',
    'http://kiva.org/lend/995544'
       ]

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/"
    "JCForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "JCVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "JCSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combinedfeaturesUse",
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
    if "#JobCreator" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
