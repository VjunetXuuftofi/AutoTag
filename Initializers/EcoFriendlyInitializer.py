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

Creates a csv relating loan uses to whether or not the loan should receive #Eco-friendly. This is useful for the Bag of
Words approach.
"""

import csv

writer = csv.writer(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/EcoFriendlyBagOfWords.csv", "w+"))

correct = 0
total = 0

ids = []
loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
for loan in loans:
    if loan["Partner Name"] == "One Acre Fund":
        continue
    if "#Eco-friendly" in loan["Tags"]:
        writer.writerow([loan["Loan ID"], loan["Use"], 1])
    else:
        writer.writerow([loan["Loan ID"], loan["Use"], 0])
