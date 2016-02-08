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
Switched to Bag of Words approach.
"""



import csv
from Other import Analysis
import pickle
import numpy as np

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging.csv"))
forest = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/AForest", "rb"))
vectorizer = pickle.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/AVectorizer", "rb"))

probabilities = []
for loan in loans:
    use = loan["Use"]
    modified = [Analysis.modify(use)]
    if modified != [None]:
        modified = vectorizer.transform(modified).toarray()
        prediction = forest.predict_proba(modified)
        if np.mean(probabilities) > 0.0095:
            if prediction[0][0] > 0.01:
                continue
            else:
                probabilities.append(prediction[0][0])
                print(np.mean(probabilities))
        else:
            if prediction[0][0] > 0.02:
                continue
            else:
                probabilities.append(prediction[0][0])
                print(np.mean(probabilities))
    else:
        continue
    if "#Animals" in loan["Tags"]:
        correct += 1
    else:
        print("http://www.kiva.org/lend/" + loan["Loan ID"])
    total += 1
    print(correct, total)

