import requests
from bs4 import BeautifulSoup
import cloudscraper
import time
import datetime
import random
from updateData import getData, updateData, pasteData, logData
import traceback
def getVotecount(page1, page2, URL):
  try:
    start_time = time.perf_counter()
    random.seed()
    #masterURL = "https://hypixel.net/threads/hypixel-mafia-halloween-in-january-town-win-game-xlviii.3770594/"
    oldTag = ""
    votecount = {}
        #get list of alive voters:
    scraper = cloudscraper.create_scraper()
    response = scraper.get(URL).text
    """from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    #import undetected_chromedriver.v2 as uc

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    response = driver.page_source
"""
    soup = BeautifulSoup(response, 'html.parser')
    cycle = ""
    title = soup.find(class_="p-title-value").get_text()
    if(title.lower().find("day") != -1):
      cycle = "Day "+ title[title.lower().find("day")+4:title.lower().find("day")+5]
    elif(title.lower().find("night") != -1):
      cycle = "Night "+title[title.lower().find("night")+6:title.lower().find("night")+7]
    print(title)
    print("_"+cycle+"_")
    #print(soup.encode("utf-8"))
    message = soup.find_all("article", class_='message')[0]

    text = (message.find(class_='bbWrapper')).get_text()

    text = text[text.lower().find("spoiler: living players"):text.lower().find("spoiler: dead players")]
    #print(text.encode("utf-8"))

    while(text.find("@") != -1):
        text = text[text.find("@"):]
        player = text[text.find("@")+1:text.find('\n')]
        while player[-1] == " ":
          player = player[:-1]
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

            tag1 = text.rfind("[unvote]")
            tag2 = text.rfind("[/unvote]")
            if (tag2 > tag1 and tag2 >=0 and tag1 >= 0):
                target = (text[tag1+6:tag2])
                text=text[tag2+9:]
                votecount.update({voter:"Not voting"})
    #            print(text)

            tag1 = text.rfind("[vote]")
            tag2 = text.rfind("[/vote]")

            try:
              hostname = getData("hostname").lower()
            except:
              hostname = "bob"
            if (tag2 > tag1 and tag2 != -1 and tag1 != -1) and voter.lower() != hostname:
                print("Found vote: ")
            #    print(text)
                target = (text[tag1+6:tag2])
                votecount.update({voter:target.replace(" ", '')})
                #print(text)

    #            print(text)
        i = i+1

        time.sleep(2+random.random()*2)

    text2 = {}
    print(votecount)
    for key in votecount:
        voted = votecount[key]

        if voted in text2:
            text2[voted] = text2[voted] + ", " + key

        else:
            text2[voted] = key
    format = (cycle + " Votecount:\n")
    for key in text2:
        if key != "Not voting": #skip not voting, do it last
          format = format+(("("))
          format = format+str(text2[key].count(', ')+1)
          format = format+(") " + key +": ")
          format = format+(text2[key] + '\n')
    key = "Not voting" #print list of players not voting
    if key in text2.keys():
      format = format+(("("))
      format = format+str(text2[key].count(', ')+1)
      format = format+(") " + key +": ")
      format = format+(text2[key] + '\n')

    print(format + "_")
    #driver.quit()
    #updateData("last_page_number_scanned",i)
    end_time = time.perf_counter()
    logData(page1,i,(page2 - page1) * 4.1 + 13.4,end_time-start_time)
    return(format)
  except:
    traceback.print_exc()
    errorMessage = traceback.format_exc()
    pasteURL = pasteData(errorMessage + "\n\n\n\n\n" + str(soup))
    updateData(("Error " + datetime.datetime.now().isoformat()),pasteURL)
    return("""Sorry, there was an error. Is the URL correct, and are the page number(s) right?
    \nIt's also possible the Hypixel website is a bit slow; check back in a bit. The error traceback info has been stored; see $votecount info to diagnose. See Pastebin URL: """ + pasteURL + " for html source code at fail instance.")
#getVotecount(1,2,"https://hypixel.net/threads/hypixel-mini-mafia-16-souls-day-3.4220544/")
