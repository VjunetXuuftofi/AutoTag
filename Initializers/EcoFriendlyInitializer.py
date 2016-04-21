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

Initializes machine learning tools to help tag #Eco-friendly.
"""

import csv
import pickle
from Other import Analysis

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions_combined2.csv"))
labels = []
toremove = []
for i, loan in enumerate(loans):
    activity = loan["Activity"]
    if loan["Partner Name"] == "One Acre Fund" or (
                (loan["Partner Name"] == "iDE Cambodia"
                 or loan["Partner Name"] == "TerraClear Development")
            and "water filter" in loan["Use"]):
        toremove.append(i)
        continue
    if activity == "Used Clothing" or activity == "Used Shoes" \
            or activity == "Bicycle Sales" \
            or activity == "Renewable Energy Products" \
            or activity == "Recycled Materials" \
            or activity == "Recycling":
        toremove.append(i)
        continue
    if "#Eco-friendly" in loan["Tags"]:
        labels.append(1)
    else:
        labels.append(0)
forest, vectorizer, selector = Analysis.initialize(
    "loans_assigned_for_tagging_with_descriptions_combined2", labels,
    "Use", toremove, 250, class_weight="balanced")
pickle.dump(forest, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/EFForest",
    "wb+"))
pickle.dump(vectorizer, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "EFVectorizer",
    "wb+"))
pickle.dump(selector, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "EFSelector",
    "wb+"))
