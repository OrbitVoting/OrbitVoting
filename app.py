from main import central
import time

sleepDuration = 2 #Duration between votecounts, in hours
y = 15

while(x < y): #Loops over a set number of times, every set number of hours
    print("Process Began!")

    central()
    print("Process finished.")
    print("Sleeping " + sleepDuration + " hours.")
    time.sleep(sleepDuration * 3600)
    y = y+1
