import time
import traceback
import gspread
from pbwrap import Pastebin
import json

import os
from replit import db
from inspect import getsourcefile
from os.path import abspath

def getToken(tokenName):

        #set active directory to app location
    directory = abspath(getsourcefile(lambda:0))
    #check if system uses forward or backslashes for writing directories
    if(directory.rfind("/") != -1):
        newDirectory = directory[:(directory.rfind("/")+1)]
    else:
        newDirectory = directory[:(directory.rfind("\\")+1)]
    os.chdir(newDirectory)

    f = open("tokens.json")
    data = json.load(f)
    return data[tokenName]

#Pastebin stuff to dump error data
def pasteData(text):
  api_dev_key = getToken("pastebin")
  username = getToken("pastebin_username")
  password = getToken("pastebin_password")

  pastebin = Pastebin(api_dev_key)
  pastebin.authenticate(username, password)
  url = pastebin.create_paste(text, api_paste_private=2, api_paste_name=None, api_paste_expire_date=None, api_paste_format=None)
  return(url)

def getData(key):
  i = 0
  while(1):
    i=i+1
    if(2**i>64):
      return "failure"
    try:
      if(key == "delay"):
        return float(db[key])
      else:
        return(db[key])
    except KeyError:
      print("Database error: could not find value of _" + key + "_. Set value to 0.")
      updateData(key,"0")
    except: #Likely a rate-limiting error for repl.it database?
      traceback.print_exc()
      time.sleep(2**i)
      print("Exception caught. Will sleep for " + str(2**i) + " seconds and retry.")

def updateData(key, value):
    if(key=="delay"):
      db[key] = str(value)
    else:
      db[key] = value
    return
def listData():
  format = ("Stored data:\n")

  for key in db.keys():
        format = format + key + ": " + str(db[key]) + "\n"

  return format

def logData(firstPage,lastPage,ETA,ATA):
    gc = gspread.service_account(filename="googleKey.json")
    sh = gc.open_by_url("""https://docs.google.com/spreadsheets/d/1-zi9sXDdfwzczTf0b_y779wV4BL6onPn-yEQpnRo-IQ/edit#gid=0""")
    worksheet = sh.sheet1
    i=0
    all_values = worksheet.get_all_values()
    for row in all_values:
        if(row[0]==''):
            break
        i = i+1
    i=i+1

    worksheet.update('A'+str(i),lastPage-firstPage)
    worksheet.update('B'+str(i),ETA)
    worksheet.update('C'+str(i),ATA)
    return
def clearErrors():
  for key in db.keys():
    if(key.find("Error")==0):
      del db[key]
  return
