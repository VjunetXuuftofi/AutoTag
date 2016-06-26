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

Gets a list of all partners
"""
import requests
import json
import pickle
fpdict = json.loads(requests.get(
    "http://api.kivaws.org/v1/partners.json").text)
fplist = []
for a in fpdict["partners"]:
    if a["status"] == "active":
        fplist.append(a["name"])
print(fplist)
pickle.dump(fplist,
            open("/Users/thomaswoodside/PycharmProjects/AutoTag/DataFiles"
                 "/fplist", "wb+"))
