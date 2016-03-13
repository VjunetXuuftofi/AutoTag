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

Creates a csv relating loan descriptions to whether or not the loan should receive #Refugee. Then feeds this data to
the initializer in Analysis.py and saves the results to pickle files.
"""

import csv
from Other import Analysis
import pickle

writer = csv.writer(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/BagOfWords/RBagOfWords.csv", "w+"))
writer.writerow(["id", "description", "value"])
ids = []
loans = csv.DictReader(open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/loans_assigned_for_tagging_with_descriptions_combined.csv"))
for loan in loans:
    if "#Refugee" in loan["Tags"]:
        writer.writerow([loan["Loan ID"], loan["Description"], 1])
    else:
        writer.writerow([loan["Loan ID"], loan["Description"], 0])

forest, vectorizer, selector = Analysis.initialize("R", [150, 2])
pickle.dump(forest, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/RForest", "wb+"))
pickle.dump(vectorizer, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/RVectorizer", "wb+"))
pickle.dump(selector, open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/RSelector", "wb+"))
