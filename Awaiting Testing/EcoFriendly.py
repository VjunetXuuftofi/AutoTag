import requests
import json
import time
from datetime import datetime
from time import mktime
from datetime import timedelta
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
