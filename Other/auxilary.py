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

All interactions with the internet happen here. Includes methods to pull data from the Kiva API as well as identify and
tag loans.
"""

import requests
import json
from selenium import webdriver
import time
from collections import defaultdict
import re
from tqdm import tqdm
from datetime import timedelta
from datetime import datetime
import psutil

chromedriver = "/Users/thomaswoodside/Dropbox/chromedriver"
driver = webdriver.Chrome(chromedriver)

def kivatag(taglist):
    """
    Uses Selenium to sign into kiva and tag loans given in taglist through the Firefox webdriver.
    :param taglist:
    """
    if len(taglist) < 1:
        print("No new loans to tag.")
        return None
    print("Commencing Tagging")
    driver.get("https://www.kiva.org/login")
    try:
        elem = driver.find_elements_by_tag_name("input")
        elem[0].send_keys("autotaggingkiva@gmail.com")
        elem[1].send_keys("dummyaccount\n")
        time.sleep(2)
    except:
        pass
    for loan in tqdm(taglist):
        driver.get("https://www.kiva.org/lend/" + str(loan))
        try:
            elem = driver.find_element_by_xpath("//*[@id='loanTagListing']/div[2]/a")
            elem.click()
        except:
            try:
                elem = driver.find_element_by_xpath("//*[@id='noLoanTagsListing']/a")
                elem.click()
            except:
                pass
        toexclude = []
        try:
            existingtags = driver.find_element_by_id("tagSelections")
            existingtag = existingtags.find_elements_by_tag_name("span")
            for tag in existingtag:
                toexclude.append(str(tag.get_attribute("class"))[4:])
        except:
            pass
        elems = driver.find_elements_by_class_name("loanTagCheckbox")
        for tag in taglist[loan]:
            if tag in toexclude:
                continue
            for elem in elems:
                try:
                    elem = elem.find_element_by_id(tag)
                    elem.click()
                except:
                    pass
            time.sleep(1)
    print("Done Tagging.")


def getinfo(IDs):
    """
    Pulls and returns data about specific loans from the Kiva API.
    Includes a time sleep to ensure that usage limits aren't exceeded.
    No more than 100 loan ID
    :param IDs:
    :return loans:
    """
    response = requests.get("http://api.kivaws.org/v1/loans/" + IDs + ".json",
                 params = {"appid" : "com.woodside.autotag"})
    time.sleep(1)
    loans = json.loads(response.text)["loans"]
    return loans


def determinetags(loans):
    """
    Takes a complete list of loan objects and determines which tags each one should have, storing this in a defaultdict.
    Then, feeds this data to taglist for tagging.
    :param loans:
    """
    print("Determining the tags that each loan should have.")
    conversions = {
        "one" : "1",
        "two" : "2",
        "three" : "3",
        "four" : "4",
        "five" : "5",
        "six" : "6",
        "seven" : "7",
        "eight" : "8",
        "nine" : "9",
        "ten" : "10",
        "eleven" : "11",
        "twelve" : "12",
        "thirteen" : "13",
        "fourteen" : "14",
        "fifteen" : "15",
        "sixteen" : "16",
        "seventeen" : "17",
        "eighteen" : "18",
        "nineteen" : "19"
    }
    tags = defaultdict(list)
    for page in loans:
        for loan in page:
            loanid = loan["id"]
            description = loan["description"]["texts"]["en"]
            use = loan["use"]
            sector = loan["sector"]
            if loan["partner_id"] == 202:
                tags[loanid].append("8")
                tags[loanid].append("9")
                numborrowers = len(loan["borrowers"])
                try:
                    pos = re.findall("a total of ([^ ]*?) solar lights.?", description)[0]
                    if pos in conversions:
                        pos = conversions[pos]
                    if int(pos) > 0.5 * numborrowers:
                        tags[loanid].append("38")
                except:
                    pass
            match = re.findall(" ([1-9][1-9]) (years old|years of age|year old|year\-old)", description)
            if len(match) > 0:
                if int(match[0][0]) >= 50:
                    tags[loanid].append("13")
            for match in ["fabric", "sewing", "tailor", "dressmaking", "weaving", "embroidery", "batik", "basketry", "pagnes",
           "Elei", "elei"]:
                if len(re.findall(" " + match + "[^A-z]", use)) > 0:
                    tags[loanid].append("26")
            if sector == "Health" or "health" in use or "latrine" in use or " sanita" in use or "toilet" in use:
                if sector != "Agriculture" and sector != "Retail":
                    tags[loanid].append("27")
            if sector == "Education":
                tags[loanid].append("18")
    kivatag(tags)


def getquery(form, lasttime = None):
    """
    Takes in an HTTP form and submits this form with the Kiva API. All data from the form is returned as a list of
    dictionaries. Optionally, a datetime object can be included to stop getting more information once that data is older
    than the query.
    :param form:
    :param lasttime:
    :return queryresults:
    """
    queryresults = []
    info = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    info = json.loads(info)
    for i in range(1, int(info["paging"]["pages"])):
        form["page"] = str(i)
        response = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form)
        time.sleep(1)
        loans = json.loads(response.text)["loans"]
        queryresults.append(loans)
        if (lasttime):
            out = False
            for loan in loans:
                postedtime = datetime.fromtimestamp(time.mktime(time.strptime(loan["posted_date"], "%Y-%m-%dT%H:%M:%SZ")))
                if lasttime - postedtime > timedelta(microseconds = 1):
                    out = True
                    break
            if out:
                break
    return queryresults