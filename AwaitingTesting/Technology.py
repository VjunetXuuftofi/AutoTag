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

System and testing for tagging loans with #Technology.
Testing 1/31 success @ 100%
"""



import csv
import re

looking = ["telephone", "TV", "mobile phone", "mobile money", "computer", "internet", "printing", "M-pesa",
           "mobile airtime", "biodigester", "solar home system", "cell phone",
           "telephones", "TVs", "mobile phones", "computers", "biodigesters", "solar home systems",
           "cell phones"]

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
for loan in loans:
    use = loan["Use"]
    escape = True
    if loan["Partner Name"] == "One Acre Fund":
        continue
    for match in looking:
        if len(re.findall(" " + match + "[^A-z]", use)) > 0:
                escape = False
                break
    if escape:
        if loan["Partner Name"] != "PT Rekan Usaha Mikro Anda (Ruma)":
            continue
    if "#Technology" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Raw Link"], use)
    total += 1
print(correct, total)

