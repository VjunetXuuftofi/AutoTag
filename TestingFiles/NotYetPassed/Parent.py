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
from TestingFiles.Deployed import GetAge

correct = 0
total = 0
ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_new.csv"))

pforest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/PForest", "rb"))
pvectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/PVectorizer", "rb"))
pselector = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/PSelector", "rb"))
rightpredictions = 0
wrongpredictions = 0

idlist = ["http://kiva.org/lend/1015472", "http://kiva.org/lend/1013436", "http://kiva.org/lend/1011773",
          "http://kiva.org/lend/1011817", "http://kiva.org/lend/1010300", "http://kiva.org/lend/1010764",
          "http://kiva.org/lend/1010502", "http://kiva.org/lend/1008137", "http://kiva.org/lend/1010622",
          "http://kiva.org/lend/1008937", "http://kiva.org/lend/993421", "http://kiva.org/lend/1007695",
          "http://kiva.org/lend/1007587", "http://kiva.org/lend/1007496", "http://kiva.org/lend/1006923",
          "http://kiva.org/lend/1006925", "http://kiva.org/lend/1007209", "http://kiva.org/lend/1006600",
          "http://kiva.org/lend/1006405", "http://kiva.org/lend/1005509", "http://kiva.org/lend/1006344",
          "http://kiva.org/lend/998371", "http://kiva.org/lend/1001551", "http://kiva.org/lend/999536",
          "http://kiva.org/lend/997552", "http://kiva.org/lend/997840", "http://kiva.org/lend/1000298",
          "http://kiva.org/lend/998155", "http://kiva.org/lend/997822", "http://kiva.org/lend/995397",
          "http://kiva.org/lend/994946", "http://kiva.org/lend/993860", "http://kiva.org/lend/997148",
          "http://kiva.org/lend/993492", "http://kiva.org/lend/994692", "http://kiva.org/lend/990945",
          "http://kiva.org/lend/990753", "http://kiva.org/lend/992733", "http://kiva.org/lend/988764",
          "http://kiva.org/lend/986207", "http://kiva.org/lend/987630", "http://kiva.org/lend/987997",
          "http://kiva.org/lend/987824", "http://kiva.org/lend/986828", "http://kiva.org/lend/1012386",
          "http://kiva.org/lend/1011833", "http://kiva.org/lend/1012981", "http://kiva.org/lend/1012148",
          "http://kiva.org/lend/1009494", "http://kiva.org/lend/1001130", "http://kiva.org/lend/998197",
          "http://kiva.org/lend/997683", "http://kiva.org/lend/1000155", "http://kiva.org/lend/996278",
          "http://kiva.org/lend/994091", "http://kiva.org/lend/993464", "http://kiva.org/lend/993315",
          "http://kiva.org/lend/987787", "http://kiva.org/lend/1012593", "http://kiva.org/lend/1011291",
          "http://kiva.org/lend/1008213", "http://kiva.org/lend/1009563", "http://kiva.org/lend/1004678",
          "http://kiva.org/lend/999195", "http://kiva.org/lend/996528", "http://kiva.org/lend/997211",
          "http://kiva.org/lend/994226", "http://kiva.org/lend/989012",  "http://kiva.org/lend/993213",
          "http://kiva.org/lend/991778", "http://kiva.org/lend/988674", "http://kiva.org/lend/1013598",
          "http://kiva.org/lend/1011225", "http://kiva.org/lend/1002014", "http://kiva.org/lend/997113",
          "http://kiva.org/lend/993787", "http://kiva.org/lend/988402", "http://kiva.org/lend/1012612",
          "http://kiva.org/lend/1013568", "http://kiva.org/lend/1000081", "http://kiva.org/lend/987023",
          "http://kiva.org/lend/1009467", "http://kiva.org/lend/1006965", "http://kiva.org/lend/990107",
          "http://kiva.org/lend/1014007", "http://kiva.org/lend/998297", "http://kiva.org/lend/992963",
          "http://kiva.org/lend/1009880", "http://kiva.org/lend/1007950", "http://kiva.org/lend/1004295",
          "http://kiva.org/lend/1028000", "http://kiva.org/lend/1027191", "http://kiva.org/lend/1026815",
          "http://kiva.org/lend/1026491", "http://kiva.org/lend/1025811", "http://kiva.org/lend/1025759",
          "http://kiva.org/lend/1025743", "http://kiva.org/lend/1024910", "http://kiva.org/lend/1024698",
          "http://kiva.org/lend/1024623", "http://kiva.org/lend/1024622", "http://kiva.org/lend/1024603",
          "http://kiva.org/lend/1026968", "http://kiva.org/lend/1023856", "http://kiva.org/lend/1023814"
          ]

for loan in tqdm(loans):
    age = GetAge.GetAge(loan["Description"])
    if age and age >= 50:
            continue
    modified = [Analysis.modify(loan["Description"])]
    if modified != [None]:
        pmodified = pvectorizer.transform(modified)
        pmodified_and_selected = pselector.transform(pmodified).toarray()
        pprediction = pforest.predict_proba(pmodified_and_selected)
    else:
        continue
    if pprediction[0][1] < 0.75:
        continue
    if "#Parent" in loan["Tags"] or "#SingleParent" in loan["Tags"]:
        rightpredictions += pprediction[0][1]
        correct += 1
    else:
        wrongpredictions += pprediction[0][1]
        if loan["Raw Link"] not in idlist:
            print("Parent", loan["Raw Link"])
    total += 1
    print(correct, total)
    try:
        print(correct/total)
        print(rightpredictions/correct)
        print(wrongpredictions/(total-correct))
    except:
        pass
