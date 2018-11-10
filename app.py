from main import central
import time

while(True):
    print("Process Began!")

    central()
    print("Process finished.")
    time.sleep(3600*2)
    print("Good!")
