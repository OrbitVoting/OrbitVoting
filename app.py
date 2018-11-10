from main import central
import time

sleepDuration = 2 #Duration between votecounts, in hours

while(True):
    print("Process Began!")

    central()
    print("Process finished.")
    print("Sleeping " + sleepDuration + " hours.")
    time.sleep(sleepDuration * 3600)
