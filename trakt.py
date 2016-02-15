#! /usr/bin/env python3

import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")
if not config["token"]["access_token"]:
    print("Open the link in a browser and paste the pincode when prompted:")
    print("https://trakt.tv/oauth/authorize?response_type=code&client_id={0}&"
          "redirect_uri=urn:ietf:wg:oauth:2.0:oob".format(
              config["token"]["client_id"]))
    pincode = input("enter pincode:")
    url = "https://api-v2launch.trakt.tv/oauth/token"
    values = {
        "code": pincode,
        "client_id": config["token"]["client_id"],
        "client_secret": config["token"]["client_secret"],
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code"
    }

    req = requests.post(url, data=values)
    resp = req.json()

    config["token"]["access_token"] = resp["access_token"]
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + config["token"]["access_token"],
    'trakt-api-version': '2',
    'trakt-api-key': config["token"]["client_id"]
}

showname = input("enter show name:")
season_no = int(input("enter season number:"))
episode = int(input("enter episode number:"))
url = "https://api-v2launch.trakt.tv/calendars/my/shows/"
date = "2016-02-11"
days = "7"
resp = requests.get(url + date + "/" + days, headers=headers)
print(resp.status_code)
jso = resp.json()
vals = {}
for val in jso:
    if showname.lower() in val["show"]["title"].lower():
        vals["shows"] = [val["show"]]
        vals["shows"][0]["seasons"] = [{}]
        vals["shows"][0]["seasons"][0]["number"] = season_no
        vals["shows"][0]["seasons"][0]["episodes"] = [{}]
        vals["shows"][0]["seasons"][0]["episodes"][0][
            "watched_at"] = "2016-02-15T14:30:10.000Z"
        vals["shows"][0]["seasons"][0]["episodes"][0]["number"] = episode
        break


url_sync = "https://api-v2launch.trakt.tv/sync/history"

rep = requests.post(url_sync, data=json.dumps(vals), headers=headers)
print(rep.json(), rep.status_code)
