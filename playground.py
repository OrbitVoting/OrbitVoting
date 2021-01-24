import requests
from bs4 import BeautifulSoup
import time
def getVotecount(page1, page2, URL):
    votecount = {}
    i = page1
    #URL = URL[:URL.rfind('/')]
    URL = URL.replace("https://", "")
    masterURL = "https://"+URL + "page-"
    while(i <= page2):
        print(i)
        URL = masterURL + str(i)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        for message in soup.find_all("article", class_='message'):
            for quote in (message.find_all("blockquote")):
                quote.clear()
            voter = ((message.find(class_='username')).contents)[0]
            text = (message.find(class_='bbWrapper')).get_text()
            text = text.lower()
            #print(text)


            tag1 = text.rfind("[vote]")
            tag2 = text.rfind("[/vote]")
            if (tag2 > tag1 and tag2 != -1 and tag1 != -1):
                print("Found vote: ")
            #    print(text)
                target = (text[tag1+6:tag2])
                votecount.update({voter:target.replace(" ", '')})
                #print(text)
            tag1 = text.rfind("[unvote]")
            tag2 = text.rfind("[/unvote]")
            if (tag2 > tag1 and tag2 >=0 and tag1 >= 0):
                target = (text[tag1+6:tag2])
                votecount.update({voter:"Not voting"})
    #            print(text)
        i = i+1

        time.sleep(2)

    text2 = {}
    print(votecount)
    for key in votecount:
        voted = votecount[key]

        if voted in text2:
            text2[voted] = text2[voted] + ", " + key

        else:
            text2[voted] = key
    format = ("Votecount:\n")
    for key in text2:
        format = format+(("("))
        format = format+str(text2[key].count(', ')+1)
        format = format+(") " + key +": ")
        format = format+(text2[key] + '\n')
    #print(text2)
    print(format)

    return(format)
#getVotecount(111,189,"https://hypixel.net/threads/hypixel-mafia-halloween-in-january-day-2.3770594/")
