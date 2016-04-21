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

System and testing for tagging loans with #WomanOwnedBiz.
Testing 1/31 failed @ 97.3%
Switched to Bag of Words approach.
"""
from tqdm import tqdm
import csv
import pickle

correct = 0
total = 0
ids = ["http://kiva.org/lend/1014412", "http://kiva.org/lend/1014045",
       "http://kiva.org/lend/1014380",
       "http://kiva.org/lend/1013267", "http://kiva.org/lend/1013298",
       "http://kiva.org/lend/1013165",
       "http://kiva.org/lend/1011785", "http://kiva.org/lend/1010627",
       "http://kiva.org/lend/1010225",
       "http://kiva.org/lend/1010245", "http://kiva.org/lend/1010142",
       "http://kiva.org/lend/1009747",
       "http://kiva.org/lend/1008103", "http://kiva.org/lend/1009667",
       "http://kiva.org/lend/1010504",
       "http://kiva.org/lend/1009593", "http://kiva.org/lend/1008905",
       "http://kiva.org/lend/1006898",
       "http://kiva.org/lend/1006848", "http://kiva.org/lend/1005150",
       "http://kiva.org/lend/1004962",
       "http://kiva.org/lend/1004745", "http://kiva.org/lend/1003960",
       "http://kiva.org/lend/1004048",
       "http://kiva.org/lend/999098", "http://kiva.org/lend/997065",
       "http://kiva.org/lend/1012400",
       "http://kiva.org/lend/1005636", "http://kiva.org/lend/1005547",
       "http://kiva.org/lend/1004537",
       "http://kiva.org/lend/1004036", "http://kiva.org/lend/996665",
       "http://kiva.org/lend/996666",
       "http://kiva.org/lend/1012330", "http://kiva.org/lend/1010236",
       "http://kiva.org/lend/1005671",
       "http://kiva.org/lend/1005019", "http://kiva.org/lend/1004678",
       "http://kiva.org/lend/996929",
       "http://kiva.org/lend/996528", "http://kiva.org/lend/1010445",
       "http://kiva.org/lend/1010904",
       "http://kiva.org/lend/996689", "http://kiva.org/lend/1013958",
       "http://kiva.org/lend/1000300",
       "http://kiva.org/lend/1010627", "http://kiva.org/lend/1010204",
       "http://kiva.org/lend/1010142",
       "http://kiva.org/lend/1008103", "http://kiva.org/lend/1010504",
       "http://kiva.org/lend/1008905",
       "http://kiva.org/lend/1004745", "http://kiva.org/lend/999098",
       "http://kiva.org/lend/1000300",
       "http://kiva.org/lend/997727", "http://kiva.org/lend/997065",
       "http://kiva.org/lend/997501",
       "http://kiva.org/lend/990244", "http://kiva.org/lend/1029191",
       "http://kiva.org/lend/1028591",
       "http://kiva.org/lend/1028463", "http://kiva.org/lend/1027559",
       "http://kiva.org/lend/1027569",
       "http://kiva.org/lend/1027038", "http://kiva.org/lend/1026994",
       "http://kiva.org/lend/1023344",
       "http://kiva.org/lend/1023588", "http://kiva.org/lend/1021511"]

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_new.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/VForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/VVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/VSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_newfeaturesDescription",
    "rb"))
for i, loan in enumerate(tqdm(loans)):
    if loan["Partner Name"] == "One Acre Fund" or loan["Sector"] == "Housing":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .7:
            continue
    else:
        continue
    if "#Vegan" in loan["Tags"]:
        correct += 1
    else:
        desc = loan["Description"]
        if loan["Raw Link"] not in ids:
            print(loan["Raw Link"])
            for sentence in loan["Description"].split("."):
                print(sentence)
    total += 1
    print(correct, total)
    print(correct / total)
