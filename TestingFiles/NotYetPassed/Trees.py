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

System and testing for tagging loans with #Trees.
Testing 1/31 failed @ 93.75%
Planning to switch to the Bag of Words approach.
"""



import csv
import re

looking = ["trees", "apple", "apricot", "avocado", "cacao", "calamondin", "calamansi", "carob", "cherry", "custard apple",
           "sugar apple", "coconut", "durian", "fig", "guava", "grapefruit", "jocote", "jackfruit", "lemon", "lime",
           "longan", "mango", "mulberry", "nance", "necterine", "olive", "orange", "papaya", "peach", "persimmon",
           "pitaya", "dragonfruit", "plum", "pomegranate", "tamarillo", "tree tomato", "almond", "cashew", "chestnut",
           "hazelnut", "pistachio", "almacigo", "banana", "copperwood", "cork", "eucalyptus", "falcata",
           "laurel", "paulownia", "resin", "tagua palm", "ivory palm", "ivory-nut palm", "tara"]

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
for loan in loans:
    use = loan["Use"]
    escape = True
    if loan["Sector"] != "Agriculture":
        continue
    for match in looking:
        if len(re.findall(" " + match + "[^A-z]", use)) > 0:
                escape = False
                break
    if escape:
        continue
    if "#Trees" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Raw Link"], use, loan["Activity"])
    total += 1
print(correct, total)

