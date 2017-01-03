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

Useful for performing data cleaning and adding specific tags to large
batches of loans.
"""

import csv
from selenium import webdriver
from tqdm import tqdm
import os


def addtags(filenames, ids, tag):
    """
    Saves new tags in
    :param filenames: A list of filenames to retrieve data from.
    :param ids: A list of loan ids on which to add the tag.
    :param tag: The tag to add to all of the loans given in ids.
    """
    for file in filenames:
        newfile = []
        with open(file) as f:
            loans = csv.DictReader(f)
            for loan in loans:
                if loan["Loan ID"] in ids:
                    print("added")
                    loan["Tags"] += ", " + tag
                newfile.append(loan)
            towrite = csv.DictWriter(open(file, "w+"),
                                     fieldnames=["Loan ID", "Name", "Raw Link",
                                                 "Loan Link For Excel",
                                                 "Popularity", "Loan Amount",
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
                                                 "Country", "Sector",
                                                 "Activity", "Use", "Tags",
                                                 "Repayment Interval",
                                                 "Repayment Term",
                                                 "Translator Byline",
                                                 "Themes", "Ray Number",
                                                 "Ray Total", "Ray Array",
                                                 "Loan Tagger",
                                                 "Assigned On (UTC)",
                                                 "Description", "Women", "RB"])
            towrite.writerows(newfile)
            f.close()


def startManualCleaning(badloans):
    """
    Takes a list of possibly unclean loans and cycles through it in firefox,
    allowing the user to mark loans for modification by the modify function.
    :param badloans: A list of possibly mistagged loans.
    """
    driver = webdriver.Chrome("/Users/thomaswoodside/Dropbox/chromedriver 3")
    goodlist = []
    badlist = []
    print(badloans)
    for loan in tqdm(badloans):
        driver.get(loan)
        response = input("For loan " + loan + ": ")
        if response == "y":
            goodlist.append(loan)
        else:
            badlist.append(loan)
        print(goodlist)
        print(badlist)
    driver.quit()

def saveBadLoans(badloans, key, info):
    file = open(os.path.abspath("./DataFiles/Badloans/" + key), "w+")
    file.writelines(info)
    file.writelines(str(badloans))

if __name__ == "__main__":
    #startManualCleaning({'1113532', 
    # '1101153', '1100973', '1064842', '1123606', '1126538', '1104027', '1074480', '1091295', '1120560', '1077424', '1108960', '1106025', '1095985'})
    addtags([
        "/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles/"
        "loans_assigned_for_tagging_with_descriptions_combined6.csv"
    ],
        ['1126538', '1104027',
         '1074480', '1077424'],
        "#Repair Renew Replace")

#"Loan ID","Name","Raw Link","Loan Link For Excel","Popularity","Loan Amount","Funded Amount","Amount Needed","Percent Funded","Lars Ratio","Time Left (Seconds)","Funding Rate Per Hour","Posted Date (UTC)","Planned Expiration Date (UTC)","Disbursed Date (UTC)","Posted Date (US/Pacific)","Planned Expiration Date (US/Pacific)","Disbursal Date (US/Pacific)","Time Left","Partner Name","Partner Link","Partner Delinquency Rate","Partner Default Rate","Partner Total Amount Raised","Partner No. of Loans Posted","Partner Loans At Risk Rate","Partner Currency Exchange Loss Rate","Partner Portfolio Yield","Partner Rating","Partner Secular Rating","Partner Social Rating","Partner Religious Affiliation","Country","Sector","Activity","Use","Tags","Repayment Interval","Repayment Term","Translator Byline","Themes","Ray Number","Ray Total","Ray Array","Loan Tagger","Assigned On (UTC)","Description","Women","RB"
