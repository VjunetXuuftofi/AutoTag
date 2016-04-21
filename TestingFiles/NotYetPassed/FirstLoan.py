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

System for testing machine learning tools for #FirstLoan.
"""
from tqdm import tqdm
import csv
import pickle

correct = 0
total = 0
ids = ["http://kiva.org/lend/1029246", "http://kiva.org/lend/1026299",
       "http://kiva.org/lend/1024742",
       "http://kiva.org/lend/1025228", "http://kiva.org/lend/1023452",
       "http://kiva.org/lend/1021229",
       "http://kiva.org/lend/1019335", "http://kiva.org/lend/1021210",
       "http://kiva.org/lend/1026808",
       "http://kiva.org/lend/1023571", "http://kiva.org/lend/1021833",
       "http://kiva.org/lend/1017152",
       "http://kiva.org/lend/1026295", "http://kiva.org/lend/1025201",
       "http://kiva.org/lend/1025227",
       "http://kiva.org/lend/1023193", "http://kiva.org/lend/1023190",
       "http://kiva.org/lend/1023157",
       "http://kiva.org/lend/1021465", "http://kiva.org/lend/1021467",
       "http://kiva.org/lend/1021469",
       "http://kiva.org/lend/1021472", "http://kiva.org/lend/1019262",
       "http://kiva.org/lend/1025700",
       "http://kiva.org/lend/1021208", "http://kiva.org/lend/1021881",
       "http://kiva.org/lend/1019296",
       "http://kiva.org/lend/1021471", "http://kiva.org/lend/1013790",
       "http://kiva.org/lend/1012289",
       "http://kiva.org/lend/1005281", "http://kiva.org/lend/998490",
       "http://kiva.org/lend/996811",
       "http://kiva.org/lend/996076", "http://kiva.org/lend/989695",
       "http://kiva.org/lend/989323",
       "http://kiva.org/lend/986965", "http://kiva.org/lend/1010080",
       "http://kiva.org/lend/992516",
       "http://kiva.org/lend/989799", "http://kiva.org/lend/986955",
       "http://kiva.org/lend/996797",
       "http://kiva.org/lend/992499", "http://kiva.org/lend/990364",
       "http://kiva.org/lend/987040",
       "http://kiva.org/lend/994978", "http://kiva.org/lend/994832",
       "http://kiva.org/lend/994845",
       "http://kiva.org/lend/992502", "http://kiva.org/lend/986910",
       "http://kiva.org/lend/1028190",
       "http://kiva.org/lend/999013", "http://kiva.org/lend/1014733"]

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_combined.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/FLForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/FLVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/FLSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_combinedfeaturesDescription",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if loan["RB"] == "1":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .5:  # .7
            continue
        print(prediction[0][1])
    else:
        continue
    if "#FirstLoan" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)
