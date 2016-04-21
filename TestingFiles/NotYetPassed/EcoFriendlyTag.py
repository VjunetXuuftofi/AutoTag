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

System for testing machine learning tools for tagging #Eco-friendly.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = ['http://kiva.org/lend/1005903', 'http://kiva.org/lend/995019',
       'http://kiva.org/lend/998465',
       'http://kiva.org/lend/1004618', 'http://kiva.org/lend/1006328',
       'http://kiva.org/lend/990371', 'http://kiva.org/lend/1005913',
       'http://kiva.org/lend/1005325',
       'http://kiva.org/lend/1014652',
       'http://kiva.org/lend/1019081', 'http://kiva.org/lend/1006560',
       'http://kiva.org/lend/1006566',
       'http://kiva.org/lend/994496', 'http://kiva.org/lend/992733',
       'http://kiva.org/lend/999874',
       'http://kiva.org/lend/1043763', 'http://kiva.org/lend/994367',
       'http://kiva.org/lend/1016924',
       'http://kiva.org/lend/999173', 'http://kiva.org/lend/1035420',
       'http://kiva.org/lend/1033704',
       'http://kiva.org/lend/999870', 'http://kiva.org/lend/1043885',
       'http://kiva.org/lend/1048033',
       'http://kiva.org/lend/1040084', 'http://kiva.org/lend/1040978',
       'http://kiva.org/lend/998754',
       'http://kiva.org/lend/1020235', 'http://kiva.org/lend/1040984',
       'http://kiva.org/lend/1039589',
       'http://kiva.org/lend/1024103', 'http://kiva.org/lend/1038494',
       'http://kiva.org/lend/1042856',
       'http://kiva.org/lend/1045255', 'http://kiva.org/lend/1034593',
       'http://kiva.org/lend/1043639',
       'http://kiva.org/lend/1008155', 'http://kiva.org/lend/1039731',
       'http://kiva.org/lend/1006795',
       'http://kiva.org/lend/1011464', 'http://kiva.org/lend/1015527',
       'http://kiva.org/lend/1016926',
       'http://kiva.org/lend/1021511', 'http://kiva.org/lend/1006575',
       'http://kiva.org/lend/1041681',
       'http://kiva.org/lend/1039743', 'http://kiva.org/lend/988096',
       'http://kiva.org/lend/1016936',
       'http://kiva.org/lend/1040990', 'http://kiva.org/lend/1046432',
       'http://kiva.org/lend/1046227',
       'http://kiva.org/lend/1021470', 'http://kiva.org/lend/988102',
       'http://kiva.org/lend/1035296',
       'http://kiva.org/lend/1038597', 'http://kiva.org/lend/1023725',
       'http://kiva.org/lend/1019449',
       'http://kiva.org/lend/992740', 'http://kiva.org/lend/994550',
       'http://kiva.org/lend/999004',
       'http://kiva.org/lend/1023728', 'http://kiva.org/lend/1007773',
       'http://kiva.org/lend/1043527',
       'http://kiva.org/lend/1009071', 'http://kiva.org/lend/987703',
       'http://kiva.org/lend/994313',
       'http://kiva.org/lend/1043750', 'http://kiva.org/lend/1019258',
       'http://kiva.org/lend/1012086',
       'http://kiva.org/lend/1028634', 'http://kiva.org/lend/1026576',
       'http://kiva.org/lend/1008208', 'http://kiva.org/lend/1012542',
       'http://kiva.org/lend/1013655',
       'http://kiva.org/lend/1046386', 'http://kiva.org/lend/1027745',
       'http://kiva.org/lend/1011215',
       'http://kiva.org/lend/1036270', 'http://kiva.org/lend/1028471',
       'http://kiva.org/lend/1012625',
       'http://kiva.org/lend/1027671', 'http://kiva.org/lend/1043514',
       'http://kiva.org/lend/1040094', 'http://kiva.org/lend/1043548',
       'http://kiva.org/lend/1013924', 'http://kiva.org/lend/991755',
       'http://kiva.org/lend/1045084',
       'http://kiva.org/lend/1022230',
       'http://kiva.org/lend/1040322', 'http://kiva.org/lend/999921',
       'http://kiva.org/lend/999922',
       'http://kiva.org/lend/999928', 'http://kiva.org/lend/999926',
       'http://kiva.org/lend/1043559',
       'http://kiva.org/lend/1021537']

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/EFForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "EFVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "EFSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2featuresUse",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    activity = loan["Activity"]
    if loan["Partner Name"] == "One Acre Fund" or (
                (loan["Partner Name"] == "iDE Cambodia" or
                    loan["Partner Name"] == "TerraClear Development") and
                "water filter" in loan["Use"]):
        continue
    if activity == "Used Clothing" or activity == "Used Shoes" \
            or activity == "Bicycle Sales" \
            or activity == "Renewable Energy Products" \
            or activity == "Recycled Materials" or activity == "Recycling":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .75:
            continue
        print(prediction[0][1])
    else:
        continue
    if "#Eco-friendly" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
