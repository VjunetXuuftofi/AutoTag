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

Helps to pull data from the Kiva API.
"""

import json
import time
import requests


def getinfo(IDs):
    """
    Pulls and returns data about specific loans from the Kiva API.
    Includes a time sleep to ensure that usage limits aren't exceeded.
    :param IDs: A list of up to 100 loan ids to get info for.
    :return loans: A list of dictionaries containing the full information.
    """
    response = requests.get("http://api.kivaws.org/v1/loans/" + IDs + ".json",
                            params={"appid": "com.woodside.autotag"})
    time.sleep(60 / 55)
    loans = json.loads(response.text)["loans"]
    return loans
