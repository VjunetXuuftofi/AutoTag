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

System and testing for tagging loans with #Fabrics.
Testing 1/31 success @ 100%
This testing file is no longer necessary (the system has been deployed).
"""



import csv
import re

looking = ["fabric", "sewing", "tailor", "dressmaking", "weaving", "embroidery", "batik", "basketry", "pagnes",
           "Elei", "elei"]

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_new.csv"))
for loan in loans:
    use = loan["Use"]
    escape = True
    for match in looking:
        if len(re.findall(" " + match + "[^A-z]", use)) > 0:
            escape = False
            break
    if escape:
        continue
    if "#Fabrics" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Raw Link"], use)
    total += 1
    print(correct, total)

