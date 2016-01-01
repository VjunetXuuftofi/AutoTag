import csv



looking = ["goat", "dairy", "cow", "calf", "calves", "chicken", "chicks", "buffalo", "rabbit", "sheep", "duck", "pig",
           "duckling", "lamb", "cattle", "bull", "ram", "poultry", "honey", "bee", "animal", "livestock",
           "ox", "steer", "heifer", "turkey", "hen", "piglet",
           "goats", "cows", "chickens", "chicks", "buffalos", "rabbits", "ducks", "pigs", "ducklings", "lambs",
           "bulls", "rams", "bees", "animals", "oxen", "steers", "heifers", "turkeys", "sows", "hens", "piglets"]


correct = 0
total = 0

ids = []

loans = csv.DictReader(open("loans_assigned_for_tagging.csv"))
for loan in loans:
    use = loan["use"]
    escape = True
    for match in looking:
        if match in use:
            escape = False
            break
    if escape:
        continue
    if match == "dairy" or match == "chicken" or match == "animal" or match == "chickens" or match == "animals"\
            or match == "hen" or match == "hens":
        if loan["Sector"] != "Agriculture":
            continue
    if loan["Activity"] == "Butcher Shop":
        continue
    if "#Animals" in loan["tags"]:
        correct += 1
    total += 1
