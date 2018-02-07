-from __future__ import print_function
import praw
import time
import traceback
from config_calliphibot import *
from config_tsmexcusebot import *
import datetime
from datetime import datetime
import logging
import os
from pprint import pprint
import threading
import sys
import json,urllib.request,codecs,requests

##july 21st 
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('eventLog.txt', 'a'))
print = logger.info

users_textfile = open('usersknown.txt', 'r+')
users_list = users_textfile.read().split()
master_list = []


recipient="WindforceJanna"
tsm = praw.Reddit(user_agent=tsm_user_agent,
                         client_id=tsm_client_id,
                         client_secret=tsm_client_secret,
                         username=tsm_username,
                         password=tsm_password)

commented_textfile = open('commented.txt', 'r+')
commented_list = commented_textfile.read().split()


r = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret,
                         username=my_username,
                         password=my_password)




stopTask = False

## this one is for testing only
def function1():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through submissions of /r/JannaMains.")
    for submission in r.subreddit("Jannamains").submissions():
        if submission.score < 7:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Low score post found! Removing " + str(submission.title))
            submission.mod.remove(spam=False)

    

                    


## this one checks for duplicates
def function2():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through directory of known users.")
    users_list.sort()
    for i in range(0,len(users_list)-1):
        if users_list[i] == users_list[i+1]:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S: ') + str(users_list[i]) + ' is a duplicate')
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")


## this one gathers the names of all new flair users, posters, and commenters of /r/Janna
def function3():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through flair users of /r/Janna.")
    for item in r.subreddit('Janna').flair(limit=None):
        if item['user'] not in users_list:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": New flair user found! Adding " + str(item['user']) + " to the directory.")
            users_list.append(str(item['user']))
            users_textfile.seek(0,2)
            users_textfile.write(str(item['user']) + ' ')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")
        else:
            pass
    
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through submitters of /r/Janna.")
    for submission in r.subreddit("Janna").submissions():
        if str(submission.author) not in users_list:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": New poster found! Adding " + str(submission.author) + " to the directory.")
            users_list.append(str(submission.author))
            users_textfile.seek(0,2)
            users_textfile.write(str(submission.author) + ' ')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")

        else:
            pass

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through commenters of /r/Janna.")
    for comment in r.subreddit("Janna").comments(limit=None):
        if str(comment.author) not in users_list:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": New commenter found! Adding " + str(comment.author) + " to the directory.")
            users_list.append(str(comment.author))
            users_textfile.seek(0,2)
            users_textfile.write(str(comment.author) + ' ')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")
        else:
            pass

    


## this one is a supporting method for function4
def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                for child_val in item_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                yield item_val


## this one looks at archived posts of /r/leagueoflegends
def function4():
    count = 1
    for item in os.listdir(r'C:\Users\Waffle\Dropbox\calliphibot\leagueoflegends 01-08-2016 01-12-2016'):
        with open(os.path.join(r'C:\Users\Waffle\Dropbox\calliphibot\leagueoflegends 01-08-2016 01-12-2016', item)) as data_file:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": opening " + item)
            redditPost = json.load(data_file)
            for author in item_generator(redditPost, "author"):
                if str(author) not in master_list:
                    try:
                        for comment in r.redditor(author).comments.new(limit=None):
                            if str(comment.subreddit).lower() == "leagueoflegends":
                                try:
                                    if comment.author_flair_css_class.lower() == "janna":
                                        if str(author) not in users_list:
                                            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": New commenter/poster found! Adding " + author + " to the list and message sent")
                                            r.redditor(str(author)).message("Invitation to the Janna community", "Hey " +str(comment.author)+"!\n\nI noticed that you have a Janna flair in the League subreddit. Assuming you like her as a champion, I'd like to introduce you to /r/Janna, a community for all Janna mains and enthusiasts. Thank you for your time. <3\n\nVery respectfully,  \nserendina")
                                            users_list.append(str(author))
                                            users_textfile.seek(0,2)
                                            users_textfile.write(str(author) + ' ')
                                        else:
                                            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + author + " already knows about the community")
                                    else:
                                        print(author+" no janna flair.")
                                    break
                                except:
                                    print(author+" no flair at all")
                                    break
                    except:
                        print(author + " bad reddit account")
                    master_list.append(str(author))
        
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": closing " + item)
        os.remove(r'C:\Users\Waffle\Dropbox\calliphibot\leagueoflegends 01-08-2016 01-12-2016\\' + item)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": removing " + item)
        if count >= 50:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": moving on to next function")
            break
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": finished reading through file " + str(count))
            count += 1



## this one finds people who have Janna flair on /r/leagueoflegends and sends them a message advertising /r/Janna
def function5():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Iterating through commments from /r/LoL.")
    for comment in r.subreddit("leagueoflegends").comments():
        if str(comment.author_flair_css_class) == "janna" and str(comment.author) not in users_list:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + str(comment.author) + " has made a comment and will be messaged and added to the directory.")
            comment.author.message("Invitation to the Janna community", "Hey " +str(comment.author)+"!\n\nI noticed that you have a Janna flair in the League subreddit. Assuming you like her as a champion, I'd like to introduce you to /r/Janna, a community for all Janna mains and enthusiasts. Thank you for your time. <3\n\nVery respectfully,  \nserendina")
            users_list.append(str(comment.author))
            users_textfile.seek(0,2)
            users_textfile.write(str(comment.author) + ' ')
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")

##    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Collecting posts...")
##    for post in r.subreddit("leagueoflegends").submissions():
##        if str(post.author_flair_css_class) == "janna" and str(post.author) not in users_list:
##            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + str(post.author) + " has made a post and will be messaged and added to the directory.")
##            post.author.message("Invitation to the Janna community", "Hey " +str(post.author)+"!\n\nI noticed that you have a Janna flair in the League subreddit. Assuming you like her as a champion, I'd like to introduce you to /r/Janna, a community for all Janna mains and enthusiasts. Thank you for your time. <3\n\nVery respectfully,  \nserendina")
##            users_list.append(str(post.author))
##            users_textfile.seek(0,2)
##            users_textfile.write(str(post.author) + ' ')
##            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": There are " + str(len(users_list)) + " users in the directory.")



def function6():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Retrieving leaderboard data.")
    url = "http://flairs.championmains.com/api/leaderboard?championId=40&count=-1&minPoints=21600"
    response = urllib.request.urlopen(url)
    reader = codecs.getreader("utf-8")
    jsonobj = json.load(reader(response))
    if "result" not in jsonobj:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Key \"result\" not returned.")

    finallbd = "Rank | Player | Points \n ---|---|---"
    for idx, pair in enumerate(jsonobj['result']['entries']):
        finallbd += "\n" + str(idx + 1)+ " | " + str(pair["name"]) + " | " + str(pair["totalPoints"]) 

    
    page = r.subreddit('Janna').wiki['championpoints']
    page.edit(finallbd, 'because I can')
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Updated the wiki leaderboard.")


    sidebar = ''
    midlbd = ""
    count = 0
    for idx, pair in enumerate(jsonobj['result']['entries']):
        if count < 25:
            try:        
                midlbd += "\n" + str(idx + 1)+ " | " + str(pair["name"]) + " | " + str(pair["totalPoints"])
                count += 1
            except:
                break
                
    with open('prelbd.txt', 'r') as myfile:
        prelbd=myfile.read()

    with open('postlbd.txt', 'r') as myfile:
        postlbd=myfile.read()

    sidebar = prelbd + midlbd + "\n" + postlbd 

    subreddit = r.subreddit('Janna')
    subreddit.mod.update(description=sidebar)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Updated the sidebar leaderboard.")




def function7():
    subreddit = tsm.subreddit('teamsolomid+tsm_excuse_bot')
    comments = subreddit.comments()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Running the excuse bot.")
    ##.stream.comments() for continuous monitoring
    for comment in comments:
        comment_text = comment.body.lower()

        rito1 = any(string in comment_text for string in rito1box)
        rito2 = any(string in comment_text for string in rito2box)
        rito3 = any(string in comment_text for string in rito3box)
        rito4 = any(string in comment_text for string in rito4box)
        rito5 = any(string in comment_text for string in rito5box)
        rito6 = any(string in comment_text for string in rito6box)
        rito7 = any(string in comment_text for string in rito7box)
        rito8 = any(string in comment_text for string in rito8box)
        del1 = any(string in comment_text for string in del1box)
        del2 = any(string in comment_text for string in del2box)
        del3 = any(string in comment_text for string in del3box)
        del4 = any(string in comment_text for string in del4box)
        del5 = any(string in comment_text for string in del5box)
        cla1 = any(string in comment_text for string in cla1box)
        cla2 = any(string in comment_text for string in cla2box)
        cla3 = any(string in comment_text for string in cla3box)
        cla4 = any(string in comment_text for string in cla4box)
        cla5 = any(string in comment_text for string in cla5box)
        cla6 = any(string in comment_text for string in cla6box)
        cla7 = any(string in comment_text for string in cla7box)
        cla8 = any(string in comment_text for string in cla8box)
        cla9 = any(string in comment_text for string in cla9box)
        parth1 = any(string in comment_text for string in parth1box)
        parth2 = any(string in comment_text for string in parth2box)
        parth3 = any(string in comment_text for string in parth3box)
        parth4 = any(string in comment_text for string in parth4box)
        parth5 = any(string in comment_text for string in parth5box)
        meme1 = any(string in comment_text for string in meme1box)
        meme2 = any(string in comment_text for string in meme2box)
        meme3 = any(string in comment_text for string in meme3box)
        meme4 = any(string in comment_text for string in meme4box)
        meme5 = any(string in comment_text for string in meme5box)
        other1 = any(string in comment_text for string in other1box)
        other2 = any(string in comment_text for string in other2box)
        other3 = any(string in comment_text for string in other3box)
        other4 = any(string in comment_text for string in other4box)
        other5 = any(string in comment_text for string in other5box)
        other6 = any(string in comment_text for string in other6box)
        other7 = any(string in comment_text for string in other7box)
        other8 = any(string in comment_text for string in other8box)
        other9 = any(string in comment_text for string in other9box)
        other10 = any(string in comment_text for string in other10box)

        if comment.id not in commented_list and rito1:
            comment.reply(messagebeginning+rito1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")
            
        if comment.id not in commented_list and rito2:
            comment.reply(messagebeginning+rito2_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and rito3:
            comment.reply(messagebeginning+rito3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and rito4:
            comment.reply(messagebeginning+rito4_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")
        
        if comment.id not in commented_list and rito5:
            comment.reply(messagebeginning+rito5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and rito6:
            comment.reply(messagebeginning+rito6_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and rito7:
            comment.reply(messagebeginning+rito7_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and rito8:
            comment.reply(messagebeginning+rito8_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and del1:
            comment.reply(messagebeginning+del1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and del2:
            comment.reply(messagebeginning+del2_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and del3:
            comment.reply(messagebeginning+del3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and del4:
            comment.reply(messagebeginning+del4_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and del5:
            comment.reply(messagebeginning+del5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla1:
            comment.reply(messagebeginning+cla1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla2:
            comment.reply(messagebeginning+cla2_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla3:
            comment.reply(messagebeginning+cla3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")


        if comment.id not in commented_list and cla4:
            comment.reply(messagebeginning+cla4_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla5:
            comment.reply(messagebeginning+cla5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla6:
            comment.reply(messagebeginning+cla6_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and cla7:
            comment.reply(messagebeginning+cla7_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")


        if comment.id not in commented_list and cla8:
            comment.reply(messagebeginning+cla8_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")


        if comment.id not in commented_list and cla9:
            comment.reply(messagebeginning+cla9_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and parth1:
            comment.reply(messagebeginning+parth1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and parth2:
            comment.reply(messagebeginning+parth2_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and parth3:
            comment.reply(messagebeginning+parth3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and parth4:
            comment.reply(messagebeginning+parth14_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and parth5:
            comment.reply(messagebeginning+parth5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and meme1:
            comment.reply(messagebeginning+meme1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and meme2:
            comment.reply(messagebeginning+meme2_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and meme3:
            comment.reply(messagebeginning+meme3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and meme4:
            comment.reply(messagebeginning+meme4_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and meme5:
            comment.reply(messagebeginning+meme5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")
            

        if comment.id not in commented_list and other1:
            comment.reply(messagebeginning+other1_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and other2:
            comment.reply(messagebeginning+other12_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and other3:
            comment.reply(messagebeginning+other3_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")

        if comment.id not in commented_list and other4:
            comment.reply(messagebeginning+other4_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  

        if comment.id not in commented_list and other5:
            comment.reply(messagebeginning+other5_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  

        if comment.id not in commented_list and other6:
            comment.reply(messagebeginning+other6_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  

        if comment.id not in commented_list and other7:
            comment.reply(messagebeginning+other7_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  

        if comment.id not in commented_list and other8:
            comment.reply(messagebeginning+other8_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  

        if comment.id not in commented_list and other9:
            comment.reply(messagebeginning+other9_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  


        if comment.id not in commented_list and other10:
            comment.reply(messagebeginning+other10_text+messageending)
            print("commented")
            commented_list.append(comment.id)
            commented_textfile.seek(0,2)
            commented_textfile.write(comment.id+" ")  
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Finished running the excuse bot.")
while True:
    try:
        function2()
        function3()
        function5()
        function6()
##        function7()







    except:
        traceback.print_exc()
        print('\nResuming in 10...')
        time.sleep(10)


users_textfile.close()




