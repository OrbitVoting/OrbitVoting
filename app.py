
import discord
import asyncio

from discord.ext import tasks, commands


import traceback

#OS/Directory
import os
from inspect import getsourcefile
from os.path import abspath

#json read/write
import json

from playground import getVotecount
#set active directory to app location
directory = abspath(getsourcefile(lambda:0))
newDirectory = directory[:(directory.rfind("\\")+1)]
os.chdir(newDirectory)
with open('credentials.json', 'r') as openfile:
    json_object = json.load(openfile)
TOKEN = json_object["token"]


client = discord.Client()

LIST_OF_CHANNELS = []
# URL = "blank"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await channel.send("Hello!")



@client.event
async def on_message(message):

    if message.content == "$terminate":
        channel = message.channel
        await channel.send("Loging out!")
        print("logout")
        await client.logout()

    elif message.content == "$votecount help" and message.channel.name == "botcommands":
        await message.channel.send("$votecount help: Print this help message \n $votecount url <url>: set which game you want a votecount for \n$votecount <first page> <last page>: generate vc")

    elif message.content.find("$votecount url") == 0 and message.channel.name == "botcommands":
        global URL
        URL = message.content[message.content.find("hypixel"):]
        channel = message.channel
        await channel.send("Set URL to https://" + URL)
    elif message.content == "$votecount printURL":
        await message.channel.send("URL: " + URL)

    elif message.content.find("$votecount ") == 0 and message.channel.name == "botcommands":
        channel = message.channel
        text = message.content
        p1 = text[text.find(' ')+1:text.rfind(' ')]
        text = text.replace(p1, '')
        p2 = text[text.find(' ')+2:]

        page1 = int(p1)
        page2 = int(p2)
        await channel.send("Votecount incoming. First page: " + p1 + ". Last Page: " + p2 + ". ETA: " + str((page2-page1)*2) + " seconds.")
        await channel.send("URL: " + URL)
        votecount = getVotecount(page1,page2,URL)
        await channel.send(votecount)

client.run("ODAyODE0OTQwOTg1NTU3MDEy.YA0trQ.HrcMhcp4vZCvXKKOl7KW2johQyg")
