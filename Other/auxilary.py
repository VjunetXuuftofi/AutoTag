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

Some helpful functions to be used in almost every tagging system.
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

def kivatag(taglist):
    if len(taglist) < 1:
        print("No new loans to tag.")
        return None
    print("Commencing Tagging")
    driver = webdriver.Firefox()
    driver.get("https://www.kiva.org/login")
    elem = driver.find_elements_by_tag_name("input")
    elem[0].send_keys("autotaggingkiva@gmail.com")
    elem[1].send_keys("dummyaccount\n")
    time.sleep(2)
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
    driver.quit()
    print("Done Tagging.")

def getinfo(IDs):
    """Pulls data about specific loans from the Kiva API.
    Includes a time sleep to ensure that usage limits aren't exceeded."""
    response = requests.get("http://api.kivaws.org/v1/loans/" + IDs + ".json",
                 params = {"appid" : "com.woodside.autotag"})
    time.sleep(1)
    loans = json.loads(response.text)["loans"]
    return loans


def explorer(FP):
    """Returns the tag breakdown of a Field Partner"""
    tags = {}

    total = 0

    form = {
        "partner" : FP,
        "page" : "1",
        "app_id" : "com.woodside.autotag"
    }
    loans = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    loans = json.loads(loans)
    for i in range(1, int(loans["paging"]["pages"])):
        page = str(i)
        form = {
        "partner" : FP,
        "page" : page,
        "app_id" : "com.woodside.autotag"
        }
        response = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form)
        loans = json.loads(response.text)
        headers = response.headers
        time.sleep(60/(int(headers["X-RateLimit-Overall-Limit"])))
        for loan in loans["loans"]:
            total += 1
            if len(loan["tags"]) > 0:
                for tag in loan["tags"]:
                    tag = tag["name"]
                    if tag != "volunteer_pick" and tag != "volunteer_like" and tag != "user_favorite":
                        try:
                            tags[tag] += 1
                        except:
                            tags[tag] = 1
    return tags, total

def determinetags(loans):
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
            if sector == "Health" or "health" in use or "latrine" in use or " sanita" in use:
                if sector != "Agriculture" and sector != "Retail":
                    tags[loanid].append("27")
            if sector == "Education":
                tags[loanid].append("18")

    kivatag(tags)



def getquery(form, lasttime = None):
    """Returns a list of dictionaries containing every loan matching a given query."""
    toreturn = []
    info = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form).text
    info = json.loads(info)
    for i in range(1, int(info["paging"]["pages"])):
        form["page"] = str(i)
        response = requests.get("http://api.kivaws.org/v1/loans/search.json", params=form)
        time.sleep(1)
        loans = json.loads(response.text)["loans"]
        toreturn.append(loans)
        if (lasttime):
            out = False
            for loan in loans:
                postedtime = datetime.fromtimestamp(time.mktime(time.strptime(loan["posted_date"], "%Y-%m-%dT%H:%M:%SZ")))
                if lasttime - postedtime > timedelta(microseconds = 1):
                    out = True
                    break
            if out:
                break

    return toreturn

def partnertoid(partnername):
    mapping = json.load(open("/Users/thomaswoodside/PycharmProjects/AutoTag/Other/partnermapping.json", "r"))
    return mapping[partnername]



