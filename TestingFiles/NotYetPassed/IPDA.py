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

ids = ['http://kiva.org/lend/1026507', 'http://kiva.org/lend/1006066',
       'http://kiva.org/lend/1013421', 'http://kiva.org/lend/985415',
       'http://kiva.org/lend/1023586', 'http://kiva.org/lend/1018581',
       'http://kiva.org/lend/988961', 'http://kiva.org/lend/1028625',
       'http://kiva.org/lend/999526', 'http://kiva.org/lend/1006786',
       'http://kiva.org/lend/990754', 'http://kiva.org/lend/983874',
       'http://kiva.org/lend/999928', 'http://kiva.org/lend/1020936',
       'http://kiva.org/lend/1017869', 'http://kiva.org/lend/1005205',
       'http://kiva.org/lend/1022178', 'http://kiva.org/lend/998783',
       'http://kiva.org/lend/1027008', 'http://kiva.org/lend/989821',
       'http://kiva.org/lend/1011685', 'http://kiva.org/lend/999926',
       'http://kiva.org/lend/997239', 'http://kiva.org/lend/996484',
       'http://kiva.org/lend/996368', 'http://kiva.org/lend/996495',
       'http://kiva.org/lend/1028389', 'http://kiva.org/lend/1011681',
       'http://kiva.org/lend/1006708', 'http://kiva.org/lend/1006401',
       'http://kiva.org/lend/1028680', 'http://kiva.org/lend/1011384',
       'http://kiva.org/lend/1024505']

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/"
    "IPDAForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "IPDAVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "IPDASelector",
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
    if "#IncomeProducingDurableAsset" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
