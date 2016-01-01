import csv
import auxilary
import json


total = 0
correct = 0
loans = csv.DictReader(open("loans_assigned_for_tagging.csv"))
for loan in loans:
    response = json.loads(auxilary.getinfo(loan["Loan ID"]).text)
    borrowers = response["loans"][0]["borrowers"]
    info = response["loans"][0]
    description = response["loans"][0]["description"]["texts"]["en"]
    valid = True
    for borrower in borrowers:
        if borrower["gender"] == "M":
            valid = False
            break
    if not valid:
        continue
    if "Partners in Health" in loan["Partner Name"]:
        loan["Partner Name"] = "Partners in Health"
    if "ADIM" in loan["Partner Name"]:
        loan["Partner Name"] = "ADIM"
    if "Paraguaya" in loan["Partner Name"]:
        loan["Partner Name"] = "Fundacion Paraguaya"
    if loan["Partner Name"] in ["Habitat for Humanity Mexico", "VisionFund Cambodia", "Alivio Capital",
                     "Hattha Kaksekar Limited (HKL), a partner of Save the Children", "Kenya ECLOF", "One Acre Fund",
                     "Entrepreneurs du Monde - Anh Chi Em", "SEF International", "BRAC Pakistan", "MDO Humo and Partners",
                     "VisionFund Albania", "Bai Tushum Bank CJSC", "Hekima, a partner of World Relief",
                     "M7 Microfinance Institution Limited",
                     "Urwego Opportunity Bank, a partner of Opportunity International and HOPE International",
                     "Partners in Health", "CIDRE", "Kashf Foundation", "ID Ghana", "Ibdaa Microfinance SAL",
                     "Paglaum Multi-Purpose Cooperative (PMPC)", "CAURIE Microfinance, a partner of Catholic Relief Services",
                     "ADIM", "Fundacion Paraguaya"]:
        print("Partner")
        continue
    if loan["Activity"] in ["Personal Medical Expenses", "Rickshaw", "Home Appliances",
                     "Wedding Expenses", "Consumer Goods", "Electrical Goods",
                     "Vehicle", "Auto Repair", "Electronics Sales", "Higher education costs",
                     "Laundry", "Spare Parts", "Vehicle Repairs",
                     "Taxi",
                     "Health",
                     "Farm Supplies", "Personal Purchases", "Transportation", "Fishing", "Mobile Phones",
                     "Cattle", "Farming",
                     "Butcher Shop", "Milk Sales",
                     "Motorcycle Transport", "Animal Sales", "Home Energy", "Used Shoes", "Hardware", "Property",
                     "Bakery", "Dairy", "Poultry", "Agriculture", "Clothing", "Livestock"]:
        print("Activity")
        continue
    if loan["Tags"] == "":
        continue
    if "#WomanOwnedBiz" in loan["Tags"]:
        correct += 1
    total += 1
    print(correct, total, loan)
print("Accuracy: " + str(correct/total))
