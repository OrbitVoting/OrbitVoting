def calculateVC(page1, page2):
    #Selenium Modules
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException

    #os Modules
    import os
    from inspect import getsourcefile
    from os.path import abspath

    #General Modules
    import time
    import datetime

    #Find the curent file location/chdir to current location
    directory = abspath(getsourcefile(lambda:0))
    newDirectory = directory[:(directory.rfind("\\")+1)]
    os.chdir(newDirectory)

    #---------------------------------------------------------
    #Variable definitions
    findQuotes = True
    newtext = "Quote not found?"
    votecount = {}
    pageURL = "https://hypixel.net/threads/hypixel-mini-mafia-iii-logical-fallacies-edition-day-1.1857318/page-"

    #THE ABOVE URL MUST BE SET TO BE YOUR DESIRED THREAD, MINUS THE LAST LITTLE PAGE NUMBER.
    #ex. https://hypixel.net/whatever/page-3 becomes https://hypixel.net/whatever/page-

    #Obviously, keep the quotation marks in place.

    #Create chrome options for headless mode, ie without the normal chrom GUI
    options = Options()
    options.add_argument('--headless')
    PATH = ("chromedriver.exe") #The chromedriver.exe file MUST be in the Orbitvoting folder.
    driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)

    time.sleep(1)

    pageNumber = (int(page1))
    lastPage = (int(page2)) + 1

    #Loop through each page
    while pageNumber < lastPage:
        page = pageURL + str(pageNumber)

        driver.get(page) #Navigate to the page

        print("Found Site.")

        time.sleep(2)

        #variable definitions for each page
        i = 1
        i2 = 1
        findMessages = True

        #Message Loop
        #-------------------------------
        while findMessages == True: #loop through each message
            findQuotes = True
            argument = "//ol[@id='messageList']/li[" + str(i) + "]" #xpath argument

            try: #check to see if we're at the end of the page
                el=(driver.find_element_by_xpath(argument))
            except NoSuchElementException as exception:
                findMessages = False
                print("End of messages!")


            if findMessages == True:
                text = ((el.text).encode('utf-8'))
                print("Found text.")

                i2 = 1
                foundQuotes = False

                #Quote Loop
                #----------------------------
                while findQuotes == True: #find quotes and delete them from the messages

                    argument = "//ol[@id='messageList']/li[" + str(i) + "]" + "/div[@class='messageInfo primaryContent']/div[@class='messageContent']/article/blockquote[@class='messageText SelectQuoteContainer ugc baseHtml']/div[@class='bbCodeBlock bbCodeQuote'][" + str(i2) + "]/aside/blockquote[@class='quoteContainer']"

                    try: #check if there is a quote
                        el=(driver.find_element_by_xpath(argument))

                    except NoSuchElementException as exception:
                        print("Error!")
                        findQuotes = False

                        if foundQuotes == False:
                            newtext = str(text)
                            print("No Quotes found.")

                    if findQuotes == True:
                        foundQuotes = True #remove quotes
                        print("Found Quote---")
                        quote = ((el.text).encode('utf-8'))

                        text = str(text)
                        quote = str(quote)
                        quote = quote[2:((len(quote))-1)]
                        #print(text)
                        #print(quote)
                        newtext = text.replace(quote, "")
                        text = newtext

                        #print(text)

                        i2 = i2 + 1
                i = i+1
                print("!!!!")
                print(newtext)
                print("------------------------------------------")
                newtext = newtext.lower()

                #----------------------------------------
                #Find votes and unvotes
                x = newtext.rfind("[vote]")

                if x > 0:
                    tag1 = newtext.rfind("[vote]")
                    tag2 = newtext.rfind("[/vote]")

                    if(tag1 > 0 and tag2 > 0):
                        vote = (newtext[(tag1+6):(tag2)])
                        voter = (newtext[2:(newtext.find("\\"))])

                        votecount[voter] = vote.replace(" ", "")

                y = newtext.rfind("[unvote]")
                #check to make sure the unvote isn't before the vote
                if y > -1 and y > x:
                    voter = (newtext[2:(newtext.find("\\"))])
                    votecount[voter] = "Unvoted"

                    print("UNVOTE FOUND.")
                    print("y: " + str(y) + " x: " + str(x))


        pageNumber = pageNumber + 1
        #print report
    print("Votecount for page(s) " + str((pageNumber)-1) +":")

    driver.quit() #quit chrome

#--------------------------------------------------------------------------------------
#Spit out a nice Votecount

    text2 = {}
    text = votecount
    #text = {"player A":"player 1","player B":"player 1","player 1":"player 2"} #Basic original structure of votes

    for key in text:
        voted = text[key]

        if voted in text2:
            text2[voted] = text2[voted] + ", " + key

        else:
            text2[voted] = key
    print("---------------------------------")
    print(text2)


    return(str(votecount), str(text2)) #return the votelist (Called the votecount) and the votecount (Called text2)
