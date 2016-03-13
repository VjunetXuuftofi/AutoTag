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

System and testing for tagging loans with #Animals.
Testing 1/31 failed @ 97.3%
Switched to Bag of Words approach.
"""
from tqdm import tqdm
import csv
from Other import Analysis
import pickle

correct = 0
total = 0

ids = ["https://www.kiva.org/lend/1014200", "https://www.kiva.org/lend/1011267", "https://www.kiva.org/lend/1010561",
       "https://www.kiva.org/lend/1010636", "https://www.kiva.org/lend/1008725", "https://www.kiva.org/lend/999036",
       "https://www.kiva.org/lend/997683", "https://www.kiva.org/lend/999139", "https://www.kiva.org/lend/994646",
       "https://www.kiva.org/lend/992451", "https://www.kiva.org/lend/990434", "https://www.kiva.org/lend/990318",
       "https://www.kiva.org/lend/987598", "https://www.kiva.org/lend/1026756", "https://www.kiva.org/lend/1029128",
       "https://www.kiva.org/lend/1029069", "https://www.kiva.org/lend/1017299"]

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_combined.csv"))
forest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/AForest", "rb"))
vectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/AVectorizer", "rb"))
selector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/ASelector", "rb"))
for loan in tqdm(loans):
    if loan["Activity"] == "Butcher Shop" or loan["Activity"] == "Food Market" or loan["Activity"] == "Veterinary Sales"\
            or loan["Activity"] == "General Store":
        continue
    modified = [Analysis.modify(loan["Use"])]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .5:
            continue
    else:
        continue
    if "#Animals" in loan["Tags"]:
        correct += 1
    else:
        print(total, loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct/total)