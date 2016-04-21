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

System for testing machine learning tools for tagging #WomanOwnedBiz.
"""
import csv
import pickle
from tqdm import tqdm
from Other import Modify
ids = [
    "http://kiva.org/lend/1015539", "http://kiva.org/lend/1013768",
    "http://kiva.org/lend/1014179",
    "http://kiva.org/lend/1014836", "http://kiva.org/lend/1014575",
    "http://kiva.org/lend/1013075",
    "http://kiva.org/lend/1014082", "http://kiva.org/lend/1011828",
    "http://kiva.org/lend/1013745",
    "http://kiva.org/lend/1009422", "http://kiva.org/lend/1010259",
    "http://kiva.org/lend/1006786",
    "http://kiva.org/lend/1000050", "http://kiva.org/lend/993764",
    "http://kiva.org/lend/992527",
    "http://kiva.org/lend/990094", "http://kiva.org/lend/987764",
    "http://kiva.org/lend/988753",
    "http://kiva.org/lend/988792", "http://kiva.org/lend/987774",
    "http://kiva.org/lend/987638"
    "http://kiva.org/lend/987638", "http://kiva.org/lend/1012057",
    "http://kiva.org/lend/1007083",
    "http://kiva.org/lend/993022", "http://kiva.org/lend/987638",
    "http://kiva.org/lend/1011992",
    "http://kiva.org/lend/1012517", "http://kiva.org/lend/1009215",
    "http://kiva.org/lend/1015061",
    "http://kiva.org/lend/1011573", "http://kiva.org/lend/1010655",
    "http://kiva.org/lend/1008652",
    "http://kiva.org/lend/992774", "http://kiva.org/lend/1012446",
    "http://kiva.org/lend/1011778",
    "http://kiva.org/lend/1007037", "http://kiva.org/lend/1004603",
    "http://kiva.org/lend/1001697",
    "http://kiva.org/lend/995902", "http://kiva.org/lend/996121",
    "http://kiva.org/lend/996720",
    "http://kiva.org/lend/987784" "http://kiva.org/lend/989233",
    "http://kiva.org/lend/987784",
    "http://kiva.org/lend/1012850", "http://kiva.org/lend/1008072",
    "http://kiva.org/lend/1004731",
    "http://kiva.org/lend/998267", "http://kiva.org/lend/997363",
    "http://kiva.org/lend/988667",
    "http://kiva.org/lend/983773", "http://kiva.org/lend/1017823",
    "http://kiva.org/lend/1030042",
    "http://kiva.org/lend/1028994", "http://kiva.org/lend/1027446",
    "http://kiva.org/lend/1024907",
    "http://kiva.org/lend/1026702", "http://kiva.org/lend/1019599",
    "http://kiva.org/lend/1026622",
    "http://kiva.org/lend/1025753", "http://kiva.org/lend/1028436",
    "http://kiva.org/lend/1027479",
    "http://kiva.org/lend/1018151", "http://kiva.org/lend/1025149",
    "http://kiva.org/lend/1011791",
    "http://kiva.org/lend/1029087", "http://kiva.org/lend/1027687",
    "http://kiva.org/lend/1022131",
    "http://kiva.org/lend/1018717", "http://kiva.org/lend/1028883",
    "http://kiva.org/lend/1026646",
    "http://kiva.org/lend/1027446", "http://kiva.org/lend/1030042",
    "http://kiva.org/lend/1029125",
    "http://kiva.org/lend/1021167", "http://kiva.org/lend/1022034",
    "http://kiva.org/lend/1027978",
    "http://kiva.org/lend/1023540", "http://kiva.org/lend/1019078",
    "http://kiva.org/lend/1020535",
    "http://kiva.org/lend/1030092", "http://kiva.org/lend/1026649",
    "http://kiva.org/lend/1029067",
    "http://kiva.org/lend/1027422", "http://kiva.org/lend/1020207",
    "http://kiva.org/lend/1024690",
    "http://kiva.org/lend/1024741", "http://kiva.org/lend/1028265",
    "http://kiva.org/lend/1026201",
    "http://kiva.org/lend/1024789", "http://kiva.org/lend/1028511",
    "http://kiva.org/lend/1027437",
    "http://kiva.org/lend/1018968", "http://kiva.org/lend/1012361",
    "http://kiva.org/lend/1021776",
    "http://kiva.org/lend/1021693", "http://kiva.org/lend/1019031",
    "http://kiva.org/lend/1027390",
    "http://kiva.org/lend/1014870", "http://kiva.org/lend/1015857",
    'http://kiva.org/lend/1012397', 'http://kiva.org/lend/1009559',
    'http://kiva.org/lend/996913',
    'http://kiva.org/lend/1013154', 'http://kiva.org/lend/997022',
    'http://kiva.org/lend/1013344',
    'http://kiva.org/lend/1007034', 'http://kiva.org/lend/994610',
    'http://kiva.org/lend/1014314',
    'http://kiva.org/lend/996278', 'http://kiva.org/lend/1014058',
    'http://kiva.org/lend/1014007',
    'http://kiva.org/lend/995398', 'http://kiva.org/lend/1009643',
    'http://kiva.org/lend/993052',
    'http://kiva.org/lend/1010615', 'http://kiva.org/lend/1008311',
    'http://kiva.org/lend/994981',
    'http://kiva.org/lend/991313', 'http://kiva.org/lend/996748',
    'http://kiva.org/lend/988775',
    'http://kiva.org/lend/997719', 'http://kiva.org/lend/1004219',
    'http://kiva.org/lend/1014145',
    'http://kiva.org/lend/1003719', 'http://kiva.org/lend/998956',
    'http://kiva.org/lend/995844',
    'http://kiva.org/lend/1010595', 'http://kiva.org/lend/993970',
    'http://kiva.org/lend/1006790',
    'http://kiva.org/lend/1015731', 'http://kiva.org/lend/1011569',
    'http://kiva.org/lend/1014866',
    'http://kiva.org/lend/1012526', 'http://kiva.org/lend/1009530',
    'http://kiva.org/lend/1006238',
    'http://kiva.org/lend/996082', 'http://kiva.org/lend/996544',
    'http://kiva.org/lend/1008148',
    'http://kiva.org/lend/1000231', 'http://kiva.org/lend/1014642',
    'http://kiva.org/lend/1011505',
    'http://kiva.org/lend/998506', 'http://kiva.org/lend/988407',
    'http://kiva.org/lend/1013655',
    'http://kiva.org/lend/997331', 'http://kiva.org/lend/1009995',
    'http://kiva.org/lend/995920',
    'http://kiva.org/lend/994175', 'http://kiva.org/lend/1010002',
    'http://kiva.org/lend/998356',
    'http://kiva.org/lend/1001510', 'http://kiva.org/lend/997692',
    'http://kiva.org/lend/1014572',
    'http://kiva.org/lend/1008412', 'http://kiva.org/lend/1011308',
    'http://kiva.org/lend/995340',
    'http://kiva.org/lend/1014220', 'http://kiva.org/lend/1011376',
    'http://kiva.org/lend/999002',
    'http://kiva.org/lend/1013566', 'http://kiva.org/lend/999137',
    'http://kiva.org/lend/985174',
    'http://kiva.org/lend/1005545', 'http://kiva.org/lend/994989',
    'http://kiva.org/lend/1007117',
    'http://kiva.org/lend/1010597', 'http://kiva.org/lend/1012618',
    'http://kiva.org/lend/994682', 'http://kiva.org/lend/1011560',
    'http://kiva.org/lend/1012692',
    'http://kiva.org/lend/1010579', 'http://kiva.org/lend/1006197',
    'http://kiva.org/lend/1011681',
    'http://kiva.org/lend/999325', 'http://kiva.org/lend/987729',
    'http://kiva.org/lend/991606',
    'http://kiva.org/lend/988695', 'http://kiva.org/lend/1013987',
    'http://kiva.org/lend/1012401',
    'http://kiva.org/lend/1012863', 'http://kiva.org/lend/993801',
    'http://kiva.org/lend/1015295',
    'http://kiva.org/lend/1007848', 'http://kiva.org/lend/1011367',
    'http://kiva.org/lend/1012764', 'http://kiva.org/lend/1012757',
    'http://kiva.org/lend/1014202',
    'http://kiva.org/lend/1006407', 'http://kiva.org/lend/1008103',
    'http://kiva.org/lend/992291',
    'http://kiva.org/lend/1013553', 'http://kiva.org/lend/1011608',
    'http://kiva.org/lend/1011745', 'http://kiva.org/lend/996404',
    'http://kiva.org/lend/997211',
    'http://kiva.org/lend/997936', 'http://kiva.org/lend/1011501',
    'http://kiva.org/lend/999277',
    'http://kiva.org/lend/1005672', 'http://kiva.org/lend/1010150',
    'http://kiva.org/lend/1008012', 'http://kiva.org/lend/1015810',
    'http://kiva.org/lend/1013513', 'http://kiva.org/lend/997019',
    'http://kiva.org/lend/992822',
    'http://kiva.org/lend/1026216', 'http://kiva.org/lend/1029861',
    'http://kiva.org/lend/1025570',
    'http://kiva.org/lend/1022346', 'http://kiva.org/lend/1022973',
    'http://kiva.org/lend/1028377',
    'http://kiva.org/lend/1026474', 'http://kiva.org/lend/1022075',
    'http://kiva.org/lend/1019968',
    'http://kiva.org/lend/1021925', 'http://kiva.org/lend/1019922',
    'http://kiva.org/lend/1027600',
    'http://kiva.org/lend/1024593', 'http://kiva.org/lend/1021302',
    'http://kiva.org/lend/1029250',
    'http://kiva.org/lend/1027357', 'http://kiva.org/lend/1024929',
    'http://kiva.org/lend/1026272',
    'http://kiva.org/lend/1022029', 'http://kiva.org/lend/1020694',
    'http://kiva.org/lend/1020840',
    'http://kiva.org/lend/1019538', 'http://kiva.org/lend/1017742',
    'http://kiva.org/lend/1027288',
    'http://kiva.org/lend/1027275', 'http://kiva.org/lend/1026491',
    'http://kiva.org/lend/1020598',
    'http://kiva.org/lend/1026886', 'http://kiva.org/lend/1019943',
    'http://kiva.org/lend/1026126',
    'http://kiva.org/lend/1026129', 'http://kiva.org/lend/1029309',
    'http://kiva.org/lend/1019455',
    'http://kiva.org/lend/1027023', 'http://kiva.org/lend/1019313',
    'http://kiva.org/lend/1029273',
    'http://kiva.org/lend/1024724', 'http://kiva.org/lend/1023344',
    'http://kiva.org/lend/1026132',
    'http://kiva.org/lend/1025838', 'http://kiva.org/lend/1025860',
    'http://kiva.org/lend/1029203',
    'http://kiva.org/lend/1027185', 'http://kiva.org/lend/1026619',
    'http://kiva.org/lend/1026977',
    'http://kiva.org/lend/1021321', 'http://kiva.org/lend/1025843',
    'http://kiva.org/lend/1026534',
    'http://kiva.org/lend/1025214', 'http://kiva.org/lend/1022437',
    'http://kiva.org/lend/1020882',
    'http://kiva.org/lend/1020225', 'http://kiva.org/lend/1027226',
    'http://kiva.org/lend/1020442',
    'http://kiva.org/lend/1025775', 'http://kiva.org/lend/1018577',
    'http://kiva.org/lend/1027546',
    'http://kiva.org/lend/1025797', 'http://kiva.org/lend/1023593',
    'http://kiva.org/lend/1028610',
    'http://kiva.org/lend/1028509', 'http://kiva.org/lend/1025127',
    'http://kiva.org/lend/1026133',
    'http://kiva.org/lend/1030032', 'http://kiva.org/lend/1026789',
    'http://kiva.org/lend/1019911',
    'http://kiva.org/lend/1026826', 'http://kiva.org/lend/1027616',
    'http://kiva.org/lend/1027597',
    'http://kiva.org/lend/1020789', 'http://kiva.org/lend/1026876',
    'http://kiva.org/lend/1020425',
    'http://kiva.org/lend/1026156', 'http://kiva.org/lend/1020446',
    'http://kiva.org/lend/1026509',
    'http://kiva.org/lend/1029260', 'http://kiva.org/lend/1028536',
    'http://kiva.org/lend/1019601',
    'http://kiva.org/lend/1028760', 'http://kiva.org/lend/1022173',
    'http://kiva.org/lend/1020783',
    'http://kiva.org/lend/1030430', 'http://kiva.org/lend/1026446',
    'http://kiva.org/lend/1026502',
    'http://kiva.org/lend/1026943', 'http://kiva.org/lend/1030086',
    'http://kiva.org/lend/1023977',
    'http://kiva.org/lend/1025067', 'http://kiva.org/lend/1021653',
    'http://kiva.org/lend/1026494',
    'http://kiva.org/lend/1018738', 'http://kiva.org/lend/1025762',
    'http://kiva.org/lend/1026912',
    'http://kiva.org/lend/1021205', 'http://kiva.org/lend/1010747',
    'http://kiva.org/lend/997020',
    'http://kiva.org/lend/996479',
    'http://kiva.org/lend/1005726', 'http://kiva.org/lend/1010502',
    'http://kiva.org/lend/1001036',
    'http://kiva.org/lend/987554'

]

correct = 0
total = 0
loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_new.csv"))
forest = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/WOBForest",
    "rb"))
vectorizer = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "WOBVectorizer",
    "rb"))
selector = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "WOBSelector",
    "rb"))
features_train = pickle.load(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_newfeaturesDescription",
    "rb"))
badloans = set()
for i, loan in enumerate(tqdm(loans)):
    if loan["Women"] != "1" or loan["Sector"] in ["Education", "Housing",
                                                  "Personal Use", "Health",
                                                  "Construction"]:
        continue
    if loan["Partner Name"] in ["Ibdaa Microfinance SAL", "ID Ghana",
                                "Thanh Hoa Microfinance Institution Limited Liability",
                                "Hekima, a partner of World Relief",
                                "Interactuar",
                                "Community Economic Ventures, Inc. (CEVI), a partner of VisionFund International",
                                "Accion San Diego", "CIDRE",
                                "Vision Finance Company s.a. (VFC), a partner of World Vision International",
                                "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                                "SMEP Microfinance Bank", "Kashf Foundation",
                                "National Microfinance Bank",
                                "Apoyo Integral", "Edpyme Alternativa",
                                "Cooperativa San Jose",
                                "Association for Rural Development (ARD)",
                                "MDO Humo and Partners",
                                "Organizacion de Desarrollo Empresarial Femenino (ODEF)"
                                ]:
        continue
    modified = [features_train[i]]
    if modified != [None]:
        modified = vectorizer.transform(modified)
        modified_and_selected = selector.transform(modified).toarray()
        prediction = forest.predict_proba(modified_and_selected)
        if prediction[0][1] < .85:
            print("test")
            continue
        print(prediction[0][1])
    else:
        continue
    if "#WomanOwnedBiz" in loan["Tags"]:
        correct += 1
    else:
        if loan["Raw Link"] not in ids:
            badloans.add(loan["Raw Link"])
    total += 1
    print(correct, total)
    print(correct / total)

Modify.startManualCleaning(badloans)
