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

Initializes machine learning tools for helping to tag #WomanOwnedBiz.

"""

import csv
from Other import Analysis
import pickle

loans = csv.DictReader(open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
    "loans_assigned_for_tagging_with_descriptions.csv"))
labels = []
toremove = []
for i, loan in enumerate(loans):
    if loan["Women"] != "1" or loan["Sector"] in ["Education", "Housing",
                                                  "Personal Use", "Health",
                                                  "Construction"]:
        toremove.append(i)
        continue
    if loan["Partner Name"] in ["Ibdaa Microfinance SAL", "ID Ghana",
                                "Thanh Hoa Microfinance Institution Limited Liability",
                                "Hekima, a partner of World Relief",
                                "Interactuar",
                                "Community Economic Ventures, Inc. (CEVI), a partner of VisionFund International",
                                "Accion San Diego", "CIDRE",
                                "Vision Finance Company s.a. (VFC), a partner of World Vision International",
                                "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                                "SMEP Microfinance Bank", "Kashf Foundation",
                                "National Microfinance Bank",
                                "Apoyo Integral", "Edpyme Alternativa",
                                "Cooperativa San Jose",
                                "Association for Rural Development (ARD)",
                                "MDO Humo and Partners",
                                "Organizacion de Desarrollo Empresarial Femenino (ODEF)"
                                ]:
        toremove.append(i)
        continue
    if "#WomanOwnedBiz" in loan["Tags"]:
        labels.append(1)
    else:
        labels.append(0)
forest, vectorizer, selector = Analysis.initialize(
    "loans_assigned_for_tagging_with_descriptions", labels,
    "Description", toremove, 50)
pickle.dump(forest, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Forests/WOBForest",
    "wb+"))
pickle.dump(vectorizer, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Vectorizers/"
    "WOBVectorizer",
    "wb+"))
pickle.dump(selector, open(
    "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/Selectors/"
    "WOBSelector",
    "wb+"))
