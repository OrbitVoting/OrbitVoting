from main import central
import time

import os
from inspect import getsourcefile
from os.path import abspath

kill = True
#Find the curent file location/chdir to current location
directory = abspath(getsourcefile(lambda:0))
newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)

def setSettings():
    print("Let's get the settings ready so you can run a votecount.")
    print("")
    SPREADSHEET_ID = input(("Enter the google spreadsheet ID: (ex.1VXNu_zrOsuoRPmF72ldW_A17xlu3r3XyFaRsLd_O8HY)"))
    print("")
    pageURL = input("Enter the page URL, minus the page number at the end: (ex. hypixel.net/forums/stuff/page-)")
    print("")
    print("If something fails, it was probably because you didn't enter these values correctly.")
    return(SPREADSHEET_ID, pageURL)


print("Welcome to the Votecount bot (beta v.0.2), created and maintained by Mark. If you find any bugs, tell me immediately and a fix will be deployed. Terms of use (Which Google requires me to have) can be found at orbitvoting.github.io")
print("")
print("")


file = open("settings.txt", "r")

settings = file.readline()
file.close()

if(settings == "empty\n"):

    settings = setSettings()
    pageURL = settings[0]
    SPREADSHEET_ID = settings[1]

    file = open("settings.txt", "w")

    file.write("full!\n" + pageURL + "\n" + SPREADSHEET_ID)

    file.close()

while(kill):
    print("What do you want to do?")
    print("a) Change the settings")
    print("b) Run a votecount")
    print("c) logout of Google Account")
    print("d) Quit program")

    choicecheck = True
    while(choicecheck == True):
        choice = input("Action: (a/b/c)")
        choice = choice.lower()
        if(choice != "a" and choice != "b" and choice != "c" and choice != "d"):
            print("Invalid!")

        else:
            choicecheck = False

    if(choice == "a"):
        setSettings()

    if(choice == "b"):
        totalCyles = 5
        cycle = 0
        print('Starting cycle.')

        while(cycle < totalCyles):

            print("Starting VC!")
            returnValues = central()

            delay = (returnValues[0])
            totalCyles = (returnValues[1])
            cycle = cycle+1
            print("Done process. Sleeping " + str(delay) + " hours. Completed " + str(cycle) + " cyles out of " + str(totalCyles))
            time.sleep(delay*3600)



        print("Done cycle!")

    if(choice == "c"):
        os.remove("token.json")

    if(choice == "d"):
        kill = False
