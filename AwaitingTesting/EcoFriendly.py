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

System and testing for tagging loans with #Eco-friendly.
"""

import csv



looking = ["bees", "beehive", "apiculture", "honey", "solar", "biodigester", "used clothing", "used shoes",
           "second-hand clothing", "second-hand shoes"]

correct = 0
total = 0

ids = []
loans = csv.DictReader(open("loans_assigned_for_tagging.csv"))
for loan in loans:
    escape = True
    for keyword in looking:
        if keyword in loan["Use"]:
            escape = False
            break
    if escape:
        continue
    if loan["Tags"] == "":
        continue
    if loan["Partner Name"] == "One Acre Fund":
        continue
    if "#Eco-friendly" in loan["Tags"]:
        correct += 1
    else:
        print(loan["Sector"], loan["Use"], loan["Loan ID"])
    total += 1
    print(correct, total)
