from matplotlib import rcParams
import matplotlib.animation as animation
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import json
import requests
from collections import defaultdict
import time
import pprint
import threading
import logging
import signal
import matplotlib.pyplot as plt
import random
from itertools import count
import config
# Store in config.py
# Client_ID = "<Your Client ID>"
# Authorization = "Bearer <Insert Bearer token Here>"
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
streamer_count = defaultdict(int)


def handler(signum, frame):
    print("exiting")
    exit(1)


fig, ax = plt.subplots()


signal.signal(signal.SIGINT, handler)
pagedata = requests.get(
    "https://tmi.twitch.tv/group/user/moonmoon/chatters")
# print(pagedata)

pagedatajson = pagedata.json()
# # print(len(pagedata['chatters']['viewers']))

viewerlist = []
viewerids = []
numviewers = (pagedatajson['chatters']['viewers'])

viewers = pagedatajson['chatters']['viewers']
for x in pagedatajson['chatters']['viewers']:
    viewerlist.append(x)
viewcount = pagedatajson['chatter_count']
print("Viewcount", viewcount)


def listDiff(li1, li2):
    return (list(set(li1) - set(li2)))


composite_id_list = [viewerlist[x:x+100]
                     for x in range(0, len(viewerlist), 100)]

totallen = len(composite_id_list)
# print(totallen)


def douserids(idlist):
    print(idlist)
    try:
        logintoid = requests.get(
            'https://api.twitch.tv/helix/users/',
            {'login': idlist},
            headers={'Client-ID': config.Client_ID,
                     'Authorization': config.Authorization}
        )
        # isnt working? stays at 800
        rateleft = logintoid.headers['Ratelimit-Remaining']
        print(rateleft, " RATE LEFT logintoid")
        if (int(rateleft) < 5):
            print("sleeping 1 min because Rateleft ", rateleft)
            time.sleep(60)
        logintoidjson = logintoid.json()  # converted to easier parsing
        # print(logintoidjson)
        try:
            # print(logintoidjson)
            for x in logintoidjson['data']:
                # print(x['id'])
                viewerids.append(x['id'])
        except:
            print("missing? useridtologins")
    except requests.exceptions.Timeout as e:
        print("Timeout Error:", e)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)

    # time.sleep(.2)

# print(composite_id_list) # should be lists of 100


# create a thread pool of 4 threads
# gets the ids from usernames, does 100 in each query. change 8 to your max threads
with PoolExecutor(max_workers=8) as executor:

    # _ is the body of each page that I'm ignoring right now
    for _ in executor.map(douserids, composite_id_list):
            # print(composite_viewer_list)
        pass

# print(viewerids) # should be all the viewers

# makes it unique users so we dont call someone more than once
# although thats kind of impossible unless id's are tied to email
print(len(viewerids))
viewerids = list(set(viewerids))
print(len(viewerids))
print()

# for x in logintoid['data']:
#     print(x['id'])
#     viewerids.append(x['id'])

# uneccessary to make unique viewer for 1 channel
# viewerids=list(set(viewerids)) #makes it unique users so we dont call someone more than once

# ### COMPOSITE LIST OF VIEWERS MAKES IT 100 PER
composite_viewer_list = [viewerids[x:x+100]
                         for x in range(0, len(viewerids), 100)]


# store the user list
with open('user_listdata.json', 'w', encoding="utf-8") as f:
    json.dump(composite_viewer_list, f, ensure_ascii=False)


totallen = len(composite_viewer_list)
totaldone = 0
rateleft = 0
rcParams['axes.unicode_minus'] = False

# User follows functions Gets first 100, doesn't use cursor to get more than 100


def dotogether(userlist):
    global totaldone  # use global total number of users done
    global rateleft
    # print(userlist)
    try:
        totallen = len(userlist)
        response = requests.get(
            'https://api.twitch.tv/helix/users/follows',
            {'first': '100', 'from_id': userlist},
            headers={'Client-ID': config.Client_ID,
                     'Authorization': config.Authorization}
        )
        responsejson = response.json()  # converted to easier parsing
        rateleft = response.headers['Ratelimit-Remaining']
        print(rateleft, " RATE LEFT user follows")
        if (int(rateleft) < 10):
            print("sleeping 1 min because Rateleft ", rateleft)
            time.sleep(60)
        totaldone += 1  # add to global users
        # print(totaldone)
        try:
            if (responsejson):
                for x in responsejson['data']:
                    # print(x['to_name'])
                    streamer_count[x['to_name']] += 1
        except:
            print("Missing? followdata")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)


# create a thread pool of 4 threads
# gets the follows multithreaded, change 8 to your max threads
with PoolExecutor(max_workers=8) as executor:
    # distribute the 1000 URLs among 4 threads in the pool
    # _ is the body of each page that I'm ignoring right now
    for x in composite_viewer_list:
        print(x)
        for _ in executor.map(dotogether, x):
            # print(composite_viewer_list)
            pass


if len(streamer_count) == 0:
    print("no greater than 1")
else:
    streamer_count = sorted(streamer_count.items(),
                            key=lambda kv: kv[1], reverse=True)  # sorts the list from most to least
    # pprint.pprint(streamer_count)


# starttime = time.time()
# newviewerlist = []
# while True:
#     print("tick")
#     newviewrequest = requests.get(
#         "https://tmi.twitch.tv/group/user/moonmoon/chatters").json()
#     newviewcount = newviewrequest['chatter_count']
#     # newviewers2 = newviewrequest['chatters']['viewers']
#     # print(newviewers2)
#     # print("VIEWERLIST")
#     # print(viewerlist)
#     print("viewcount", viewcount)
#     print("viewcount", newviewcount)
#     # newviewerslistdiff = listDiff(newviewers2, viewerlist)
#     # print(newviewerslistdiff)
#     print("\n\nsleeping 10 seconds\n\n")
#     time.sleep(10)
print(totaldone)


# streamernames = [j[0] for i, j in enumerate(streamer_count)]
# streamervals = [j[1] for i, j in enumerate(streamer_count)]
# # # Pie chart
# print(streamernames)
# print(streamervals)
# sizes = [15, 30, 45, 10]
# # only "explode" the 2nd slice (i.e. 'Hogs')
# explode = (0, 0.1, 0, 0)
# # add colors
# # colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
# fig1, ax1 = plt.subplots()
# ax1.pie(streamervals, explode=None, labels=streamernames, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# # Equal aspect ratio ensures that pie is drawn as a circle
# ax1.axis('equal')
# plt.tight_layout()
# plt.show()

# streamer_count.append(totaldone)
# print(type(streamer_count))
# streamer_count=dict(streamer_count) #makes it have {} in the output
# write to json file for other data processing
with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(streamer_count, f, ensure_ascii=False)
print(totaldone, "Chatters Checked")
