from main import central
import time

sleepDuration = 2 #Duration between votecounts, in hours
y = 15
x = 0
while(x < y): #Loops over a set number of times, every set number of hours
    print("Process Began!")

    central()
    print("Process finished.")
    
    time.sleep(sleepDuration * 3600)
    x = x+1
