"""
Copyright 2016 Thomas Woodside

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://apache.org/licenses/LICENSE-2.0

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
from Other import Analysis
import pickle

correct = 0
total = 0
ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_combined.csv"))

pforest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/RForest", "rb"))
pvectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/RVectorizer", "rb"))
pselector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/RSelector", "rb"))

for loan in tqdm(loans):
    modified = [Analysis.modify(loan["Description"])]
    if modified != [None]:
        pmodified = pvectorizer.transform(modified)
        pmodified_and_selected = pselector.transform(pmodified).toarray()
        pprediction = pforest.predict_proba(pmodified_and_selected)
    else:
        continue
    if pprediction[0][1] < 0.5: #0.55
        continue
    if "#Refugee" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Raw Link"])
    total += 1
    print(correct, total)
    try:
        print(correct/total)
    except:
        pass
