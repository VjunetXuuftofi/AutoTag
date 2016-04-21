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

File to test machine learning systems for #Schooling.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify

correct = 0
total = 0

ids = ["http://kiva.org/lend/1014045", "http://kiva.org/lend/1011785",
       "http://kiva.org/lend/1011154",
       "http://kiva.org/lend/1010243", "http://kiva.org/lend/1006848",
       "http://kiva.org/lend/1004460",
       "http://kiva.org/lend/1003960", "http://kiva.org/lend/997198",
       "http://kiva.org/lend/996827",
       "http://kiva.org/lend/1014045", "http://kiva.org/lend/997231",
       "http://kiva.org/lend/997145",
       "http://kiva.org/lend/996665", "http://kiva.org/lend/996666",
       "http://kiva.org/lend/1005547",
       "http://kiva.org/lend/1005115", "http://kiva.org/lend/1004689",
       "http://kiva.org/lend/1004435",
       "http://kiva.org/lend/1004216", "http://kiva.org/lend/1009667",
       "http://kiva.org/lend/1004036",
       "http://kiva.org/lend/1027959", "http://kiva.org/lend/1027299",
       "http://kiva.org/lend/1027227",
       "http://kiva.org/lend/1024932", "http://kiva.org/lend/1024842",
       "http://kiva.org/lend/1020045",
       "http://kiva.org/lend/1019365", "http://kiva.org/lend/1019005",
       "http://kiva.org/lend/1018257",
       "http://kiva.org/lend/1017806", "http://kiva.org/lend/1017744",
       "http://kiva.org/lend/1017709",
       "http://kiva.org/lend/1017648", "http://kiva.org/lend/1017119",
       "http://kiva.org/lend/1017189",
       "http://kiva.org/lend/1005558", "http://kiva.org/lend/1024220",
       "http://kiva.org/lend/1020549",
       "http://kiva.org/lend/1009867", "http://kiva.org/lend/996929",
       "http://kiva.org/lend/1017809",
       "http://kiva.org/lend/1024297", "http://kiva.org/lend/1023471",
       "http://kiva.org/lend/1028306",
       "http://kiva.org/lend/1027644",
       'http://kiva.org/lend/1036412', 'http://kiva.org/lend/1043532',
       'http://kiva.org/lend/1038046',
       'http://kiva.org/lend/1035713', 'http://kiva.org/lend/1037953',
       'http://kiva.org/lend/1040758',
       'http://kiva.org/lend/1041923', 'http://kiva.org/lend/1041917',
       'http://kiva.org/lend/1045673',
       'http://kiva.org/lend/1035721', 'http://kiva.org/lend/1035559',
       'http://kiva.org/lend/1039460',
       'http://kiva.org/lend/1039518', 'http://kiva.org/lend/1041742',
       'http://kiva.org/lend/1035399',
       'http://kiva.org/lend/1036352', 'http://kiva.org/lend/1035672',
       'http://kiva.org/lend/1042654',
       'http://kiva.org/lend/1041760', 'http://kiva.org/lend/1035709',
       'http://kiva.org/lend/1036551',
       'http://kiva.org/lend/1035674', 'http://kiva.org/lend/1039450',
       'http://kiva.org/lend/1045827',
       'http://kiva.org/lend/1035749', 'http://kiva.org/lend/1041753',
       'http://kiva.org/lend/1035759',
       'http://kiva.org/lend/1043849', 'http://kiva.org/lend/1041908',
       'http://kiva.org/lend/1041901',
       'http://kiva.org/lend/1041925', 'http://kiva.org/lend/1035720',
       'http://kiva.org/lend/1035913',
       'http://kiva.org/lend/1040187', 'http://kiva.org/lend/1041902',
       'http://kiva.org/lend/1037019',
       'http://kiva.org/lend/1035776', 'http://kiva.org/lend/1043836',
       'http://kiva.org/lend/1041750', 'http://kiva.org/lend/1041906',
       'http://kiva.org/lend/1035824',
       'http://kiva.org/lend/1031565', 'http://kiva.org/lend/1038683',
       'http://kiva.org/lend/1035768',
       'http://kiva.org/lend/1041748', 'http://kiva.org/lend/1045859',
       'http://kiva.org/lend/1038691',
       'http://kiva.org/lend/1040110', 'http://kiva.org/lend/1043537',
       'http://kiva.org/lend/1036425',
       'http://kiva.org/lend/1036288', 'http://kiva.org/lend/1035703',
       'http://kiva.org/lend/1035125',
       'http://kiva.org/lend/1048511',
       'http://kiva.org/lend/1040747', 'http://kiva.org/lend/1038198',
       'http://kiva.org/lend/1009880',
       'http://kiva.org/lend/1019313', 'http://kiva.org/lend/1023461',
       'http://kiva.org/lend/1005839',
       'http://kiva.org/lend/1046662', 'http://kiva.org/lend/1005671',
       'http://kiva.org/lend/995339',
       'http://kiva.org/lend/1018982',
       'http://kiva.org/lend/1004666', 'http://kiva.org/lend/1004537',
       'http://kiva.org/lend/1010245',
       'http://kiva.org/lend/1036461', 'http://kiva.org/lend/1010364',
       'http://kiva.org/lend/1045709',
       'http://kiva.org/lend/1041667', 'http://kiva.org/lend/1020589',
       'http://kiva.org/lend/1011108',
       'http://kiva.org/lend/1034977', 'http://kiva.org/lend/1011747',
       'http://kiva.org/lend/1017667',
       'http://kiva.org/lend/988731', 'http://kiva.org/lend/1035563',
       'http://kiva.org/lend/1011753',
       'http://kiva.org/lend/1036491',
       'http://kiva.org/lend/1011761',
       'http://kiva.org/lend/1006315', 'http://kiva.org/lend/1027356',
       'http://kiva.org/lend/1026653']

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/"
                            "DataFiles/"
                            "loans_assigned_for_tagging"
                            "_with_descriptions_combined2.csv"))

forest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/"
                          "DataFiles/Forests/ScForest", "rb"))

vectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/"
                              "DataFiles/Vectorizers/ScVectorizer", "rb"))

selector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/"
                            "DataFiles/Selectors/ScSelector", "rb"))

features_train = pickle.load(open("/Users/thomaswoodside/PycharmProjects/"
                                  "AutoTag/DataFiles/"
                                  "loans_assigned_for_tagging"
                                  "_with_descriptions_combined2"
                                  "featuresDescription",
                                  "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if loan["Sector"] == "Education":
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .7:
            continue
        print(prediction[0][1])
    else:
        continue
    if "#Schooling" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
