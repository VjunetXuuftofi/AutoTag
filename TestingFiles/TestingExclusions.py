import sys
sys.path.insert(0, '/home/thomaswoodside/AutoTag/Other')
import GetAge


def A(loan):
    if loan["Activity"] == "Butcher Shop" or loan[
        "Activity"] == "Food Market" \
            or loan["Activity"] == "Veterinary Sales" \
            or loan["Activity"] == "General Store":
        return True
    return False


def BDA(loan):
    if loan["Sector"] == "Personal Use":
        return True
    return False


def EF(loan):
    activity = loan["Activity"]
    if loan["Partner Name"] == "One Acre Fund" or (
                (loan["Partner Name"] == "iDE Cambodia" or
                         loan["Partner Name"] == "TerraClear Development") and
                    "water filter" in loan["Use"]):
        return True
    if loan["Partner Name"] in ["African Clean Energy (ACE)", "iSmart Kenya",
                                "COCAFCAL", "PAC",
                                "Dr. Bronner's / Serendipalm",
                                "KSPPS Benteng Mikro Indonesia",
                                "Impact Carbon"]:
        return True
    if loan["Partner Name"] == "FUDECOSUR" and (activity == "Farming" or
                                                        activity == "Agriculture"):
        return True
    if activity == "Used Clothing" or activity == "Used Shoes" \
            or activity == "Bicycle Sales" \
            or activity == "Renewable Energy Products" \
            or activity == "Recycled Materials" or activity == "Recycling":
        return True
    if "solar" in loan["Use"]:
        return True
    return False


def F(loan):
    if loan["Activity"] == "Textiles":
        return True
    return False


def JC(loan):
    return False


def P(loan):
    if GetAge.GetAge(loan["Description"]) and \
                    GetAge.GetAge(loan["Description"]) >= 50:
        return True
    return False


def R(loan):
    return False


def RB(loan):
    if loan["RB"] != "0":
        return True
    if "RMCR" in loan["Partner Name"]:
        return True
    return False


def Sc(loan):
    if loan["Sector"] == "Education":
        return True
    if loan["Partner Name"] in ["Camfed Tanzania", "Camfed Zimbabwe",
                                "Camfed Ghana"]:
        return True
    return False

def S(loan):
    return False

def SP(loan):
    if GetAge.GetAge(loan["Description"]) and \
            GetAge.GetAge(loan["Description"]) >= 50:
        return True
    return False

def SF(loan):
    return False

def T(loan):
    if (loan["Partner Name"] == "One Acre Fund" and "solar light" in loan[
        "Description"]) \
            or loan["Partner Name"] in ["PT Rekan Usaha Mikro Anda (Ruma)",
                                        "African Clean Energy(ACE)",
                                        "iSmart Kenya"] \
            or (loan["Partner Name"] in ["iDE Cambodia",
                                         "TerraClear Development"] and
                "water filter" in loan["Use"]) or "solar" in loan["Use"]:
        return True
    return False

def Tr(loan):
    if loan["Partner Name"] == "One Acre Fund":
        return True
    return False

def W(loan):
    return False

def WOB(loan):
    if loan["Women"] not in ["1", 1] or loan["Sector"] in ["Education",
                                                           "Housing",
                                                           "Personal Use",
                                                           "Health",
                                                           "Construction"]:
        return True
    return False