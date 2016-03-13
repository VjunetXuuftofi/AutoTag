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
from Other import Analysis
import pickle

correct = 0
total = 0

ids = ["http://kiva.org/lend/1011101", "http://kiva.org/lend/1007690", "http://kiva.org/lend/1007496",
       "http://kiva.org/lend/1008805", "http://kiva.org/lend/1006080", "http://kiva.org/lend/997926",
       "http://kiva.org/lend/993005", "http://kiva.org/lend/991885", "http://kiva.org/lend/991887",
       "http://kiva.org/lend/1011115", "http://kiva.org/lend/999030", "http://kiva.org/lend/1012568",
       "http://kiva.org/lend/999134", "http://kiva.org/lend/996106", "http://kiva.org/lend/993793",
       "http://kiva.org/lend/992844", "http://kiva.org/lend/990281", "http://kiva.org/lend/994056",
       "http://kiva.org/lend/1010554", "http://kiva.org/lend/1010861", "http://kiva.org/lend/1008705",
       "http://kiva.org/lend/1012803", "http://kiva.org/lend/1012727", "http://kiva.org/lend/1004592",
       "http://kiva.org/lend/1001697", "http://kiva.org/lend/994730", "http://kiva.org/lend/997560",
       "http://kiva.org/lend/995583", "http://kiva.org/lend/1030088", "http://kiva.org/lend/1024093",
       "http://kiva.org/lend/1027287", "http://kiva.org/lend/1030063", "http://kiva.org/lend/1023540",
       "http://kiva.org/lend/1029111", "http://kiva.org/lend/1027457", "http://kiva.org/lend/1027422",
       "http://kiva.org/lend/1025596", "http://kiva.org/lend/1023471", "http://kiva.org/lend/1024299",
       "http://kiva.org/lend/1021308", "http://kiva.org/lend/1027561", "http://kiva.org/lend/1023624",
       "http://kiva.org/lend/1029126", "http://kiva.org/lend/1024241", "http://kiva.org/lend/1020295",
       "http://kiva.org/lend/1027437", "http://kiva.org/lend/1027438", "http://kiva.org/lend/1026902",
       "http://kiva.org/lend/1026710", "http://kiva.org/lend/1023475", "http://kiva.org/lend/1029963",
       "https://www.kiva.org/lend/1023889", "https://www.kiva.org/lend/1025969", ]

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_new.csv"))
forest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/RBForest", "rb"))
vectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/RBVectorizer", "rb"))
selector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/RBSelector", "rb"))
wronglist = set()
for loan in tqdm(loans):
    if loan["RB"] == 1:
        continue
    modified = [Analysis.modify(loan["Description"])]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .6:
            continue
    else:
        continue
    if "#RepeatBorrower" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            wronglist.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct/total)
for i, a in enumerate(wronglist):
    print(i, a)