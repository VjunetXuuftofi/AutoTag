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
Testing 1/31 failed @ 85.7%
"""

import csv
from Other import Analysis

forest, vectorizer = Analysis.initialize("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/EcoFriendlyBagOfWords.csv")
correct = 0
total = 0

ids = []
loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/loans_assigned_for_tagging.csv"))
for loan in loans:
    if loan["Partner Name"] == "One Acre Fund":
        continue
    modified = [Analysis.modify(loan["Use"])]
    if modified != [None]:
        modified = vectorizer.transform(modified).toarray()
        prediction = forest.predict_proba(modified)
        if prediction[0][0] > 0.01:
            continue
    else:
        continue
    if "#Eco-friendly" in loan["Tags"]:
        correct += 1
    else:
        print("wrong")
    total += 1
    print(correct, total)
