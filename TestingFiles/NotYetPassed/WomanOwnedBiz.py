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

idlist = [
    "http://kiva.org/lend/1015539", "http://kiva.org/lend/1013768", "http://kiva.org/lend/1014179",
    "http://kiva.org/lend/1014836", "http://kiva.org/lend/1014575", "http://kiva.org/lend/1013075",
    "http://kiva.org/lend/1014082", "http://kiva.org/lend/1011828", "http://kiva.org/lend/1013745",
    "http://kiva.org/lend/1009422", "http://kiva.org/lend/1010259", "http://kiva.org/lend/1006786",
    "http://kiva.org/lend/1000050", "http://kiva.org/lend/993764", "http://kiva.org/lend/992527",
    "http://kiva.org/lend/990094", "http://kiva.org/lend/987764", "http://kiva.org/lend/988753",
    "http://kiva.org/lend/988792", "http://kiva.org/lend/987774", "http://kiva.org/lend/987638"
    "http://kiva.org/lend/987638", "http://kiva.org/lend/1012057", "http://kiva.org/lend/1007083",
    "http://kiva.org/lend/993022", "http://kiva.org/lend/987638", "http://kiva.org/lend/1011992",
    "http://kiva.org/lend/1012517", "http://kiva.org/lend/1009215", "http://kiva.org/lend/1015061",
    "http://kiva.org/lend/1011573", "http://kiva.org/lend/1010655", "http://kiva.org/lend/1008652",
    "http://kiva.org/lend/992774","http://kiva.org/lend/1012446", "http://kiva.org/lend/1011778",
    "http://kiva.org/lend/1007037", "http://kiva.org/lend/1004603", "http://kiva.org/lend/1001697",
    "http://kiva.org/lend/995902", "http://kiva.org/lend/996121", "http://kiva.org/lend/996720",
    "http://kiva.org/lend/987784" "http://kiva.org/lend/989233", "http://kiva.org/lend/987784",
    "http://kiva.org/lend/1012850", "http://kiva.org/lend/1008072", "http://kiva.org/lend/1004731",
    "http://kiva.org/lend/998267", "http://kiva.org/lend/997363", "http://kiva.org/lend/988667",
    "http://kiva.org/lend/983773", "http://kiva.org/lend/1017823", "http://kiva.org/lend/1030042",
    "http://kiva.org/lend/1028994", "http://kiva.org/lend/1027446", "http://kiva.org/lend/1024907",
    "http://kiva.org/lend/1026702", "http://kiva.org/lend/1019599", "http://kiva.org/lend/1026622",
    "http://kiva.org/lend/1025753", "http://kiva.org/lend/1028436", "http://kiva.org/lend/1027479",
    "http://kiva.org/lend/1018151", "http://kiva.org/lend/1025149", "http://kiva.org/lend/1011791",
    "http://kiva.org/lend/1029087", "http://kiva.org/lend/1027687", "http://kiva.org/lend/1022131",
    "http://kiva.org/lend/1018717", "http://kiva.org/lend/1028883", "http://kiva.org/lend/1026646",
    "http://kiva.org/lend/1027446", "http://kiva.org/lend/1030042", "http://kiva.org/lend/1029125",
    "http://kiva.org/lend/1021167", "http://kiva.org/lend/1022034", "http://kiva.org/lend/1027978",
    "http://kiva.org/lend/1023540", "http://kiva.org/lend/1019078", "http://kiva.org/lend/1020535",
    "http://kiva.org/lend/1030092", "http://kiva.org/lend/1026649", "http://kiva.org/lend/1029067",
    "http://kiva.org/lend/1027422", "http://kiva.org/lend/1020207", "http://kiva.org/lend/1024690",
    "http://kiva.org/lend/1024741", "http://kiva.org/lend/1028265", "https://www.kiva.org/lend/1026201",
    "https://www.kiva.org/lend/1024789", "https://www.kiva.org/lend/1028511", "https://www.kiva.org/lend/1027437",
    "https://www.kiva.org/lend/1018968", "https://www.kiva.org/lend/1012361", "https://www.kiva.org/lend/1021776",
    "https://www.kiva.org/lend/1021693", "https://www.kiva.org/lend/1019031", "https://www.kiva.org/lend/1027390",

]

# Hand In Hand
# GDMPC
# NWTF
# VisionFund Ecuador
# National Microfinance Bank
# Juhudi Kilimo
# Prisma
# SMEP
# FAPE
# IMPRO
# ADIM



loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_new.csv"))
forest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/WOBForest", "rb"))
vectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/WOBVectorizer", "rb"))
selector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/WOBSelector", "rb"))
linklist = set()
for loan in tqdm(loans):
    if loan["Women"] == 0:
        continue
    # Below are some partners with relatively high rates of gender misreporting. The system can't identify this at all
    # so I eliminated these partners.
    if loan["Partner Name"] == "Emprender" or loan["Partner Name"] == "Paglaum Multi-Purpose Cooperative (PMPC)" \
            or loan["Partner Name"] == "Interactuar" \
            or loan["Partner Name"] == "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International"\
            or loan["Partner Name"] == "Apoyo Integral"\
            or loan["Partner Name"] == "Thanh Hoa Microfinance Institution Limited Liability"\
            or loan["Partner Name"] == "Vision Finance Company s.a. (VFC), a partner of World Vision International"\
            or "Pro Mujer" in loan["Partner Name"] \
            or loan["Partner Name"] == "Hekima, a partner of World Relief":  # Surprisingly
        continue
    if loan["Activity"] == "Personal Medical Expenses" or loan["Sector"] == "Personal Use" or loan["Sector"] == "Education"\
            or loan["Activity"] == "Personal Housing Expenses":
        continue
    modified = [Analysis.modify(loan["Description"])]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .65:  # Not yet adjusted upwards
            continue
    else:
        continue
    if "#WomanOwnedBiz" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in idlist:
            linklist.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct/total)
for i, a in enumerate(linklist):
    print(i, a)