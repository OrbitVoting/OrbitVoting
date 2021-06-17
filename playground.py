import requests
from bs4 import BeautifulSoup
import cloudscraper
import time
def getVotecount(page1, page2, URL):
    #masterURL = "https://hypixel.net/threads/hypixel-mafia-halloween-in-january-town-win-game-xlviii.3770594/"
    oldTag = ""
    votecount = {}
        #get list of alive voters:
    scraper = cloudscraper.create_scraper()
    response = scraper.get(URL).text
    soup = BeautifulSoup(response, 'html.parser')

    message = soup.find("article", class_='message')
    text = (message.find(class_='bbWrapper')).get_text()

    text = text[text.lower().find("spoiler: living players"):text.lower().find("spoiler: dead players")]
    #print(text.encode("utf-8"))

    while(text.find("@") != -1):
        text = text[text.find("@"):]
        player = text[text.find("@")+1:text.find('\n')]
        print(player)
        votecount.update({player:"Not voting"})
        text = text[text.find('\n'):]
    i = page1
    #URL = URL[:URL.rfind('/')]
    #return
    masterURL = URL + "page-"
    while(i <=page2):
        print(i)
        URL = masterURL + str(i)

    #    URL = "https://hypixel.net/threads/hypixel-mafia-halloween-in-january-town-win-game-xlviii.3770594/page-281"

        scraper = cloudscraper.create_scraper()
        response = scraper.get(URL).text
        soup = BeautifulSoup(response, 'html.parser')

        firstPostID = soup.find("ul", {"class": "message-attribution-opposite message-attribution-opposite--list"})
#        print(mydivs.text)

        if(oldTag == firstPostID.text):
            print("Detected end of thread")

            break;
        oldTag = firstPostID.text

        for message in soup.find_all("article", class_='message'):
            for quote in (message.find_all("blockquote")):
                quote.clear()
            voter = ((message.find(class_='username')).contents)[0]
            text = (message.find(class_='bbWrapper')).get_text()
            text = text.lower()
            #print(text.encode("utf-8"))


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
    if format.replace(" ","").replace('\n',"")=="Votecount:":
      format="No votes found."
    print(format + "_")

    return(format)
getVotecount(33,284,"https://hypixel.net/threads/hypixel-mini-mafia-16-souls-day-3.4220544/")
