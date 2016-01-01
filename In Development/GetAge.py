import json
import csv
from Other import auxilary
import re

correct = 0
total = 0

ids = []

loans = csv.DictReader(open("loans_assigned_for_tagging.csv"))
for loan in loans:
    info = json.loads(auxilary.getinfo(loan["Loan ID"]).text)
    description = info["loans"][0]["description"]["texts"]["en"]
    match = re.findall(" ([1-9][1-9]) (years old|years of age|year old|year\-old)", description)
    if len(match) == 0:
        continue
    try:
        if int(match[0][0]) < 50:
            continue
    except:
        continue
    if loan["Tags"] == "":
        continue
    if "#Elderly" in loan["Tags"]:
        correct += 1
    total += 1
    print(correct, total, match)