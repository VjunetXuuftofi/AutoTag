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

This reads in a spreadsheet of loans and creates a new spreadsheet that
includes the loan description, whether the loan is only to women,
and whether the borrower has borrowed from Kiva before.
"""

import csv
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from Other import auxilary


def addInformation(filename):
    """
    Takes in a filename for a csv of loans from kivatools and adds extra
    information.
    :param filename: Name of the bare file from kivatools.
    """
    loans = csv.DictReader(open(filename))

    loanstowrite = []
    loanids = ""
    total = 0
    everyloan = []
    for loan in tqdm(loans):
        if loan["Name"] == "Anonymous":
            continue
        loanstowrite.append(loan)
        loanids += loan["Loan ID"] + ","
        total += 1
        if total == 100:
            total = 0
            loanids = loanids[:-1]
            loanlist = auxilary.getinfo(loanids)
            loanids = ""
            everyloan.append(loanlist)
    everyloan.append(auxilary.getinfo(loanids[:-1]))
    print(everyloan)

    print(len(everyloan), "pages")
    for i in range(len(everyloan)):
        print("Starting page", i)
        for a in tqdm(range(100)):
            try:
                loanstowrite[i * 100 + a]["Description"] = everyloan[i][a][
                    "description"]["texts"]["en"]
                valid = True
                for borrower in everyloan[i][a]["borrowers"]:
                    if borrower["gender"] == "M":
                        valid = False
                        break
                if valid:
                    loanstowrite[i * 100 + a]["Women"] = 1
                else:
                    loanstowrite[i * 100 + a]["Women"] = 0
                repeatborrower = 0
                soup = BeautifulSoup(requests.get("http://www.kiva.org/lend/" +
                                                  str(everyloan[i][a]
                                                      ["id"])).text,
                                     "html.parser")
                while len(soup.find_all(id="prevLoanDetails")) > 0:
                    found = soup.find(id="prevLoanDetails")
                    for child in found.children:
                        if child.name == "a":
                            link = child["href"]
                            break
                    info = auxilary.getinfo(link.split("/")[-1])
                    if info[0]["status"] == "paid":
                        repeatborrower = 1
                        break
                    else:
                        soup = BeautifulSoup(requests.get(link).text,
                                             "html.parser")
                loanstowrite[i * 100 + a]["RB"] = repeatborrower
            except:
                break

    loanstowriteedited = []
    for loan in loanstowrite:
        if loan["Description"] != '':
            loanstowriteedited.append(loan)

    towrite = csv.DictWriter(open("/Users/thomaswoodside/PycharmProjects"
                                  "/AutoTag/DataFiles/"
                                  "loans_assigned_for_tagging"
                                  "_with_descriptions_new2.csv",
                                  "w+"),
                             fieldnames=["Loan ID", "Name", "Raw Link",
                                         "Loan Link For Excel", "Popularity",
                                         "Loan Amount",
                                         "Funded Amount", "Amount Needed",
                                         "Percent Funded", "Lars Ratio",
                                         "Time Left (Seconds)",
                                         "Funding Rate Per Hour",
                                         "Posted Date (UTC)",
                                         "Planned Expiration Date (UTC)",
                                         "Disbursed Date (UTC)",
                                         "Posted Date (US/Pacific)",
                                         "Planned Expiration Date (US/Pacific)",
                                         "Disbursal Date (US/Pacific)",
                                         "Time Left",
                                         "Partner Name", "Partner Link",
                                         "Partner Delinquency Rate",
                                         "Partner Default Rate",
                                         "Partner Total Amount Raised",
                                         "Partner No. of Loans Posted",
                                         "Partner Loans At Risk Rate",
                                         "Partner Currency Exchange Loss Rate",
                                         "Partner Portfolio Yield",
                                         "Partner Rating",
                                         "Partner Secular Rating",
                                         "Partner Social Rating",
                                         "Partner Religious Affiliation",
                                         "Country",
                                         "Sector",
                                         "Activity", "Use", "Tags",
                                         "Repayment Interval",
                                         "Repayment Term",
                                         "Translator Byline",
                                         "Themes", "Ray Number", "Ray Total",
                                         "Ray Array", "Loan Tagger",
                                         "Assigned On (UTC)",
                                         "Description", "Women", "RB"])
    towrite.writerows(loanstowriteedited)
# "Loan ID","Name","Raw Link","Loan Link For Excel","Popularity","Loan Amount","Funded Amount","Amount Needed","Percent Funded","Lars Ratio","Time Left (Seconds)","Funding Rate Per Hour","Posted Date (UTC)","Planned Expiration Date (UTC)","Disbursed Date (UTC)","Posted Date (US/Pacific)","Planned Expiration Date (US/Pacific)","Disbursal Date (US/Pacific)","Time Left","Partner Name","Partner Link","Partner Delinquency Rate","Partner Default Rate","Partner Total Amount Raised","Partner No. of Loans Posted","Partner Loans At Risk Rate","Partner Currency Exchange Loss Rate","Partner Portfolio Yield","Partner Rating","Partner Secular Rating","Partner Social Rating","Partner Religious Affiliation","Country","Sector","Activity","Use","Tags","Repayment Interval","Repayment Term","Translator Byline","Themes","Ray Number","Ray Total","Ray Array","Loan Tagger","Assigned On (UTC)","Description","Women","RB"
