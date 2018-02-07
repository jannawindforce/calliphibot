import json,urllib.request,time,codecs,requests





def function1():
    url = "http://flairs.championmains.com/api/leaderboard?championId=40&count=-1&minPoints=21600"
    response = urllib.request.urlopen(url)
    reader = codecs.getreader("utf-8")
    jsonobj = json.load(reader(response))

    finalleaderboard = "Rank | Player | Points \n ---|---|---"
    for idx, pair in enumerate(jsonobj['result']['entries']):
        finalleaderboard += "\n" + str(idx + 1)+ " | " + str(pair["name"]) + " | " + str(pair["totalPoints"]) 
    print(finalleaderboard)


    sidebar = ''
    midsub = ""
    count = 0
    for idx, pair in enumerate(jsonobj['result']['entries']):
        if count < 50:
            midsub += "\n" + str(idx + 1)+ " | " + str(pair["name"]) + " | " + str(pair["totalPoints"])
            count += 1
            
    with open('presub.txt', 'r') as myfile:
        presub=myfile.read()

    with open('postsub.txt', 'r') as myfile:
        postsub=myfile.read()

    sidebar = presub + midsub + "\n" + postsub   
    print(sidebar)

    
function1()
