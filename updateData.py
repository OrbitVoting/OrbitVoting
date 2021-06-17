import time
import traceback
#from replit import db
from pbwrap import Pastebin

#Pastebin stuff to dump error data
def pasteData(text):
  api_dev_key = "QUpxJ1i4rawMn22Xh3aXbJu8LCGJLUIb"
  username = "HyperbolicStudios"
  password = "MafiaSloth987"

  pastebin = Pastebin(api_dev_key)
  pastebin.authenticate(username, password)
  url = pastebin.create_paste(text, api_paste_private=2, api_paste_name=None, api_paste_expire_date=None, api_paste_format=None)
  return(url)

def getData(key):
  i = 0
  while(1):
    i=i+1
    if(2**i>64):
      return 1
    try:
      if key == "delay":
        return float(db[key])
      return db[key]

    except: #Likely a rate-limiting error for repl.it database?
      traceback.print_exc()
      time.sleep(2**i)
      print("Exception caught. Will sleep for " + str(2**i) + " seconds and retry.")

def updateData(key, value):
  if key == "delay":
    db[key] = str(value)
    return
  db[key] = value
  return
def listData():
  format = ("Stored data: ")
  for key in db.keys():
    format = format + key + ": " + str((db[key]))+"\n"
  return format
