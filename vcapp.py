import discord
import asyncio

from discord.ext import tasks, commands


import traceback

#OS/Directory
import os
from inspect import getsourcefile
from os.path import abspath

#json read/write

from updateData import updateData, getData, listData
from playground import getVotecount

from keep_alive import keep_alive
keep_alive()
#set active directory to app location
"""directory = abspath(getsourcefile(lambda:0))
newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)
with open('credentials.json', 'r') as openfile:
    json_object = json.load(openfile)
TOKEN = json_object["token"]
"""

client = discord.Client()

LIST_OF_CHANNELS = [843278333407002675]

async def update(text):
    for CHANNEL in LIST_OF_CHANNELS:
        try:
            channel = client.get_channel(int(CHANNEL))
            await channel.send(text)
        except:
            traceback.print_exc()

async def checkForData():
    await client.wait_until_ready()
    while not client.is_closed():

      if(getData("status") == "on"):
        print("Scanning")
        await update("Getting a votecount. This may take some time. First page: " + str(getData("firstpage")))
        votecount = getVotecount(getData("firstpage"), 1000, getData("URL"))
        await update("<@&843279495884701707> "+ votecount)
        await update("The next votecount will be processed in "+str(getData("delay")/60)+" hours.")
        print("sleeping for delay")
        await asyncio.sleep(getData("delay")*60)
        print("done sleeping for delay")
      await asyncio.sleep(20)
      print("done sleeping for 20")


# URL = "blank"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)

    print(client.user.id)
    print('------')
    game = discord.Game("$votecount help")
    await client.change_presence(status=discord.Status.idle, activity=game)


    await update("Bot turned on. AutoVC currently set to " + getData("status") + ".")
    #updateData("status","off")



@client.event
async def on_message(message):
  if (message.channel.name != "votecounts"):
    if message.content == "$votecount help":
        await message.channel.send("""
        $votecount help - prints this help message.\n
        $votecount info - prints info about the bot \n
        $votecount url <url> - sets the url of the current game.\n
        $votecount auto on <first page> - turns on the automatic votecounts, which will start at page <first page> and end at the end of the thread.\n
        $votecount auto off - turns off the automatic votecounts.
        $votecount auto delay - sets the time in minutes between automatic votecounts\n
        $votecount <first page> <last page> - manually create a votecount, going from <first page> to <last page>. <last page> can be greater than the number of pages in the thread; the bot will automatically stop at the last post. *Note that the first page may include some votes from the previous day! The bot can't tell where on the page the current day started.* \n\nAll commands must be entered in #votecounts, which is restricted to the host.\n\nDm me (Mark) if you need anything.
        """)
  elif (message.channel.name == "votecounts"):

    if message.content == "$votecount ping":
        await message.channel.send("Hello <@&843279495884701707>")
        #hereRole = msg.channel.server.roles.get('Moderator', 'here')

    if message.content == "$terminate1":
        channel = message.channel
        await channel.send("Loging out!")
        print("Loged out via terminate command")
        await client.close()

    elif message.content == "$votecount help":
        await message.channel.send("""
        $votecount help - prints this help message.\n
        $votecount info - prints info about the bot \n
        $votecount url <url> - sets the url of the current game.\n
        $votecount auto on <first page> - turns on the automatic votecounts, which will start at page <first page> and end at the end of the thread.\n
        $votecount auto off - turns off the automatic votecounts.
        $votecount auto delay - sets the time in minutes between automatic votecounts\n
        $votecount <first page> <last page> - manually create a votecount, going from <first page> to <last page>. <last page> can be greater than the number of pages in the thread; the bot will automatically stop at the last post. *Note that the first page may include some votes from the previous day! The bot can't tell where on the page the current day started.* \n\nAll commands must be entered in #votecounts .\n\nDm me (Mark) if you need anything.
        """)

    elif message.content.find("$votecount auto on") == 0:
      updateData("status","on")
      updateData("firstpage",int(message.content[18:]))
      await message.channel.send("Auto VC on, starting at page " + str(getData("firstpage")) +  " . Delay set to " + str(getData("delay")) + " minutes.")
      await message.channel.send("Getting votecount; this may take some time.")
      await message.channel.send(getVotecount(getData("firstpage"),1000,getData("URL"))+"The next votecount will be processed in "+str(getData("delay")/60) + " hours.")

    elif message.content == "$votecount auto off":
      updateData("status","off")
      await message.channel.send("Auto VC off. Use $votecount auto on <firstPage> to turn it back on.")

    elif message.content.find("$votecount auto delay") == 0:
      updateData("delay", float(message.content[22:]))
      await message.channel.send("Auto delay set to " +str(getData("delay")) + " minutes. This will take effect after the next votecount.")

    elif message.content.find("$votecount url") == 0:

        updateData("URL",message.content[message.content.find("hypixel"):])
        URL = message.content[message.content.find("hypixel"):]
        URL = URL[:URL.find("/page-")]
        URL = "https://"+URL.replace("https://","")+"/"
        updateData("URL",URL)
        await message.channel.send("Set URL to " + URL)

    elif message.content == "$votecount printURL":
        await message.channel.send("URL: " + getData("URL"))

    elif message.content == "$votecount info":
      await message.channel.send(listData())


    elif message.content.find("$votecount ") == 0:
        channel = message.channel
        text = message.content
        postNumber = -1
        while text[-1] == " ":
          text = text[:-1]
        if(text.find("#")!= -1):
            postNumber = text[text.find('#')+1:text.rfind(' ')]
        else:
            p1 = text[text.find(' ')+1:text.rfind(' ')]
        print(p1 + "_")
        text = text[text.find(p1)+len(p1):]
        print(text)
        p2 = text[text.find(' ')+1:]
        print(p2)

        page1 = int(p1)
        page2 = int(p2)
        await channel.send("Votecount incoming. First page: " + p1 + ". Last Page: " + p2 + ". ETA: " + str((page2-page1)*2+6) + " seconds.")
        URL = getData("URL")
        await channel.send("URL: " + URL)
        if(postNumber == -1):
          votecount = getVotecount(page1,page2,URL)
        else:
          votecount = getVotecount(1,page2,URL,postNumber)
        print("Returned to bot: "+votecount+"_")
        await channel.send(votecount)
client.loop.create_task(checkForData())
client.run("ODQzMDIwNzAxMjU4NjEyNzM2.YJ9yNQ.cID7FypXzmXcVKl4GTywImsE5ZA")
