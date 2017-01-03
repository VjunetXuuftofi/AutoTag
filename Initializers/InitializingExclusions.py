import sys
sys.path.insert(0, '/home/thomaswoodside/AutoTag/Other')
import GetAge


def A(loan):
    return False


def BDA(loan):
    return False


def EF(loan):
    return False


def F(loan):
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
    if "RMCR" in loan["Partner Name"]:
        return True
    return False


def Sc(loan):
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
    return False

def Tr(loan):
    if loan["Partner Name"] == "One Acre Fund":
        return True
    return False

def W(loan):
    return False

def WOB(loan):
    if loan["Women"] not in ["1", 1]:
        return True
    return False