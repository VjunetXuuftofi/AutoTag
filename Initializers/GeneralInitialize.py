import csv
import json
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import argparse
import InitializingExclusions


def initialize(test_type, filename):
    loans = csv.DictReader(open(os.path.abspath(filename)))
    info = json.load(open(os.path.abspath("../DataFiles/TagInfo/"
                                          + test_type + ".json")))
    labels = []
    toremove = []
    for i, loan in enumerate(loans):
        if eval("TestingExclusions." + test_type + "(loan)"):
            toremove.append(i)
            continue
        found = False
        for tag in info["tags"]:
            if tag in loan["Tags"]:
                labels.append(1)
                found = True
                break
        if not found:
            labels.append(0)

    features_train = pickle.load(open(os.path.abspath("../DataFiles/" +
                                                      filename + "features"
                                                      + info["type"]), "rb"))
    labels_train = pd.Series(labels)
    if toremove:
        features_train = pd.Series(
            np.delete(np.array(features_train), toremove, axis=0))
    print("Creating Vectorizer")
    vectorizer = TfidfVectorizer(stop_words="english",
                                 max_df=.5,
                                 ngram_range=(1, 3))
    print("Fitting Vectorizer")
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_train = None
    print("Creating Selector")
    selector = SelectKBest(k=18000)
    print("Fitting Selector")
    selector.fit(features_train_transformed,
                 labels_train)
    print("Transforming data")
    features_train_transformed_selected = selector.transform(
        features_train_transformed)
    features_train_transformed = None
    features_train_transformed_selected = features_train_transformed_selected.toarray()
    print("Creating Forest")
    if info["search"]:
        forest = RandomForestClassifier(min_samples_leaf=2,
                                        class_weight=info["class_weight"])
        if not info["estimators_to_test"]:
            parameters = {
                "n_estimators": [50, 150, 250],
            }
        else:
            parameters = {
                "n_estimators": info["estimators_to_test"],
            }
        forest = GridSearchCV(forest, parameters)
    else:
        forest = RandomForestClassifier(n_estimators=info["n_estimators"],
                                        min_samples_leaf=2,
                                        class_weight=info["class_weight"])
    print("Fitting Forest")
    forest.fit(features_train_transformed_selected, labels_train)
    pickle.dump(forest, open(os.path.abspath("../DataFiles/Forests/" +
                                             test_type + "Forest"), "wb"))
    pickle.dump(vectorizer, open(os.path.abspath("../DataFiles/Vectorizers/" +
                                                 test_type + "Vectorizer"),
                                 "wb"))

    pickle.dump(selector, open(os.path.abspath("../DataFiles/Selectors/" +
                                                 test_type + "Selector"),
                                 "wb"))


parser = argparse.ArgumentParser()
parser.add_argument("type")
args = parser.parse_args()
initialize(args.type,
     os.path.abspath("../DataFiles/loans_assigned_for_tagging_with_descriptions_new6.csv"))