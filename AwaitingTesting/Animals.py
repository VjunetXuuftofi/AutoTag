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
"""



import csv
from Other import Analysis
from tqdm import tqdm

looking = ["goat", "dairy", "cow", "calf", "calves", "chicken", "chicks", "buffalo", "rabbit", "sheep", "duck", "pig",
           "duckling", "lamb", "cattle", "bull", "ram", "poultry", "honey", "bee", "animal", "livestock",
           "ox", "steer", "heifer", "turkey", "hen", "piglet",
           "goats", "cows", "chickens", "chicks", "buffalos", "rabbits", "ducks", "pigs", "ducklings", "lambs",
           "bulls", "rams", "bees", "animals", "oxen", "steers", "heifers", "turkeys", "sows", "hens", "piglets"]

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
forest, vectorizer = Analysis.initialize("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/AnimalBagOfWords.csv")
for loan in loans:
    use = loan["Use"]
    '''
    escape = True
    for match in looking:
        if len(re.findall(" " + match + "[^A-z]", use)) > 0:
            escape = False
            break
    if escape:
        continue
    if "Sales" in loan["Activity"]:
        continue
    if match == "dairy" or match == "chicken" or match == "animal" or match == "chickens" or match == "animals"\
            or match == "hen" or match == "hens":
        if loan["Sector"] != "Agriculture":
            continue
    if loan["Activity"] == "Butcher Shop":
        continue
    if "slaughter" in use:
        continue
        '''
    modified = [Analysis.modify(use)]
    if modified != [None]:
        modified = vectorizer.transform(modified).toarray()
        prediction = forest.predict_proba(modified)
        if prediction[0][1] > 0.01:
            continue
    else:
        continue
    if "#Animals" in loan["Tags"]:
        correct += 1
    else:
        print("http://www.kiva.org/lend/" + loan["Loan ID"])
    total += 1
    print(correct, total)

