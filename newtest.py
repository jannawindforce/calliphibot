from __future__ import print_function
import praw
import time
import traceback
from config_calliphibot import *
import datetime
from datetime import datetime
import logging
import os
from pprint import pprint
import threading
import sys
import json,urllib.request,codecs,requests


print("retrieving leaderboard data")
url = "http://flairs.championmains.com/api/leaderboard?championId=40&count=-1&minPoints=21600"
response = urllib.request.urlopen(url)
reader = codecs.getreader("utf-8")
jsonobj = json.load(reader(response))

print(jsonobj)

finalleaderboard = "Rank | Player | Points \n ---|---|---"
for idx, pair in enumerate(jsonobj['result']['entries']):
    finalleaderboard += "\n" + str(idx + 1)+ " | " + str(pair["name"]) + " | " + str(pair["totalPoints"]) 

print(finalleaderboard)
