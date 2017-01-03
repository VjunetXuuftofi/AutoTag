import csv
import pickle
from tqdm import tqdm
import os
import sys
import json
import argparse
import TestingExclusions
sys.path.insert(0, '/home/thomaswoodside/AutoTag/Other')
import Modify


def Test(test_type, filename):
    correct = 0
    total = 0
    info = json.load(open(os.path.abspath("../DataFiles/TagInfo/"
                                          + test_type + ".json")))

    loans = csv.DictReader(open(os.path.abspath(filename)))
    forest = pickle.load(open(
        os.path.abspath("./DataFiles/Forests/" + test_type + "Forest"), "rb"))
    vectorizer = pickle.load(open(
        os.path.abspath("./DataFiles/Vectorizers/" + test_type + "Vectorizer"),
        "rb"))
    selector = pickle.load(open(
        os.path.abspath("./DataFiles/Selectors/" + test_type + "Selector"),
        "rb"))
    features_train = pickle.load(open(
        os.path.abspath(filename + "features" + info["type"]),
        "rb"))
    badloans = set()
    for i, loan in enumerate(tqdm(loans)):
        if eval("TestingExclusions." + test_type + "(loan)"):
            continue
        modified = [features_train[i]]
        if modified != [None]:
            modified = vectorizer.transform(modified)
            modified_and_selected = selector.transform(modified).toarray()
            prediction = forest.predict_proba(modified_and_selected)
            if prediction[0][1] < info["threshold"]:
                continue
            print(prediction[0][1])
        else:
            continue
        found = False
        for tag in info["tags"]:
            if tag in loan["Tags"]:
                correct += 1
                found = True
        if not found:
            if loan["Raw Link"] not in info["badloans"]:
                badloans.add(loan["Raw Link"])
        total += 1
        print(correct, total)
        print(correct / total)

    info = str(correct) + "," + str(total) + "\n" + str(correct / total)
    Modify.saveBadLoans(badloans, test_type, info)

parser = argparse.ArgumentParser()
parser.add_argument("type")
args = parser.parse_args()
Test(args.type,
     os.path.abspath("../DataFiles/loans_assigned_for_tagging_with_descriptions_new6.csv"))