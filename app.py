import discord
import asyncio
import math
from discord.ext import tasks, commands
import datetime
import traceback

#OS/Directory
import os

from updateData import updateData, getData, listData

from vcBot import getVotecount

#from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']

LIST_OF_CHANNELS = []

helpPage = """
		$votecount help - prints this help message.\n
		$votecount info - prints status info about the bot \n
		$votecount url <url> - sets the url of the current game.\n
		$votecount host <host name> - sets the host name, whose vote will not count. (So they can post example vote tags without it being counted)\n
		$votecount auto on <first page> - turns on the automatic votecounts, which will start at page <first page> and end at the end of the thread.\n
		$votecount auto off - turns off the automatic votecounts.
		$votecount auto delay <minutes>- sets the time in minutes between automatic votecounts\n
		$votecount <first page> <last page> - manually create a votecount, going from <first page> to <last page>. <last page> can be greater than the number of pages in the thread; the bot will automatically stop at the last post. *Note that the first page may include some votes from the previous day! The bot can't tell where on the page the current day started.* \n\nAll commands must be entered in #votecounts, which is restricted to the host.\n\nDm me (Mark) if you need anything.
		"""
client = discord.Client()

try:  #Check if last_time key exists; if not, create new one
	last_time = getData("last_time")
	print("Last auto votecount: " + last_time)
except:
	updateData("last_time", "2021-05-24T04:24:59.703931")
	print("Wrote new time key")


async def update(text):
	print(LIST_OF_CHANNELS)
	for CHANNEL in LIST_OF_CHANNELS:
		try:
			channel = client.get_channel(int(CHANNEL))
			await channel.send(text)
		except:
			traceback.print_exc()


async def updateStatus(status):
	game = discord.Game(status)
	await client.change_presence(status=discord.Status.online, activity=game)


async def checkForData():
	await client.wait_until_ready()
	while not client.is_closed():
		delta = (datetime.datetime.now()-datetime.datetime.fromisoformat(getData("last_time"))).seconds
		print(delta)
		if(getData("status") == "on" and delta > 3600*48): #turn off after 48 hours
			await update("The automatic votecount has been on for 48 consecutive hours. It will now turn off. Use $votecount auto on <page number> to resume, or $votecount <firstpage> <lastpage> to generate a single votecount.")
			updateData("status","off")

		if (getData("status") == "on" and delta > getData("delay") * 60):
			print("Scanning")
			await update("Getting a votecount. This may take some time. First page: " + str(getData("firstpage")))
			votecount = getVotecount(getData("firstpage"), 1000, getData("URL"))
			await update(votecount)
			await update("The next votecount will be processed in " + str(getData("delay") / 60) + " hours. You=  can view this votecount and all previous votecounts in the #votecounts channel in Discord.")
			updateData("last_time", datetime.datetime.now().isoformat())
		await asyncio.sleep(2)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	# LIST_OF_CHANNELS = []
	guilds = client.guilds
	for guild in guilds:
		for channel in guild.channels:
			if (channel.name.lower() == "votecount-game-a"
				and (not (channel.id in LIST_OF_CHANNELS))):
				LIST_OF_CHANNELS.append(channel.id)
				print(guild.name + ": " + channel.name + ": " +
					  str(channel.id))

	print(LIST_OF_CHANNELS)
	print('------')

	await updateStatus("$votecount help")
	await client.change_presence(status=discord.Status.online)
	#await update("Bot restarted. AutoVC currently set to " + getData("status") + ".")
	#updateData("status","off")


@client.event
async def on_message(message):
	#print(message.channel.id)
	#print(message.channel.id in LIST_OF_CHANNELS)
	if ((message.channel.id in LIST_OF_CHANNELS) == False):
		if message.content == "$votecount help":
			await message.channel.send(helpPage)

	elif (message.channel.id in LIST_OF_CHANNELS and message.author.id != client.user.id):

		if message.content == "$votecount vis on":
			print("Turning vis on")
			guild = message.channel.guild
			for role in guild.roles:
				print(role.name)
				if role.is_default() == True:
					everyone = role
			print(everyone.name)
			try:
				await message.channel.set_permissions(everyone,
													  read_messages=True,
													  send_messages=False)
				await message.channel.send("Visibility on!")
			except:
				await message.channel.send(
					"Error. I might not have the right permissions; double-check OAuth2."
				)
		elif message.content == "$votecount vis off":
			print("Turning vis off")
			guild = message.channel.guild
			for role in guild.roles:
				print(role.name)
				if role.is_default() == True:
					everyone = role
			print(everyone.name)
			try:
				await message.channel.set_permissions(everyone,
													  read_messages=False,
													  send_messages=False)
				await message.channel.send("Visibility off. Goodbye!")
			except:
				await message.channel.send(
					"Error. I might not have the right permissions; double-check OAuth2."
				)
		elif message.content == "$votecount ping":
			await message.channel.send("Hello <@&843279495884701707>")
			#hereRole = msg.channel.server.roles.get('Moderator', 'here')

		elif message.content == "$terminate1":
			channel = message.channel
			await channel.send("Loging out!")
			print("Loged out via terminate command")
			await client.close()

		elif message.content == "$votecount help":
			await message.channel.send(helpPage)

		elif message.content.find("$votecount auto on") == 0:
			updateData("last_time", datetime.datetime.now().isoformat())
			updateData("status", "on")
			updateData("firstpage", int(message.content[18:]))
			await message.channel.send("Auto VC on, starting at page " +
									   str(getData("firstpage")) +
									   " . Delay set to " +
									   str(getData("delay")) + " minutes.")
			await message.channel.send(
				"Getting votecount; this may take some time.")
			await message.channel.send(
				getVotecount(getData("firstpage"), 1000, getData("URL")) +
				"The next votecount will be processed in " +
				str(getData("delay") / 60) + " hours. You can view this votecount and all previous votecounts in the #votecounts channel in Discord.")

		elif message.content == "$votecount auto off":
			updateData("status", "off")
			await message.channel.send(
				"Auto VC off. Use $votecount auto on <firstPage> to turn it back on."
			)

		elif message.content.find("$votecount auto delay") == 0:
			updateData("delay", float(message.content[22:]))
			await message.channel.send("Auto delay set to " +
									   str(getData("delay")) + " minutes.")

		elif message.content.find("$votecount url") == 0:

			updateData("URL",
					   message.content[message.content.find("hypixel"):])
			URL = message.content[message.content.find("hypixel"):]
			URL = URL[:URL.find("/page-")]
			URL = "https://" + URL.replace("https://", "") + "/"
			updateData("URL", URL)
			await message.channel.send("Set URL to " + URL)

		elif message.content == "$votecount printURL":
			await message.channel.send("URL: " + getData("URL"))

		elif message.content == "$votecount info":
			await message.channel.send(listData())

		elif message.content.find("$votecount announce") == 0:
			await update(message.content[20:])
		elif message.content.find("$votecount host") == 0:
			hostname = message.content[16:]
			updateData("hostname", hostname)
			await update("Host name set to \"" + hostname +
						 "\". Their votes will not count anymore.")
		elif message.content.find("$votecount ") == 0:
			channel = message.channel
			text = message.content
			postNumber = -1
			while text[-1] == " ":
				text = text[:-1]
			if (text.find("#") != -1):
				postNumber = text[text.find('#') + 1:text.rfind(' ')]
			else:
				p1 = text[text.find(' ') + 1:text.rfind(' ')]
			#print(p1 + "_")
			text = text[text.find(p1) + len(p1):]
			print(text)
			p2 = text[text.find(' ') + 1:]
			print(p2)
			page1 = int(p1)
			page2 = int(p2)
			await channel.send("Votecount incoming. First page: " + p1 +
							   ". Last Page: " + p2 + ". ETA: " +
							   (str(math.floor(((page2-page1)*4.1+13.4)/60)) + " minutes, " + str(math.floor(((page2-page1)*4.1+13.4)%60)) + " seconds"))
			#await updateStatus("Getting votecount...")
			URL = getData("URL")
			await channel.send("URL: " + URL)
			if (postNumber == -1):
				votecount = getVotecount(page1, page2, URL)
			else:
				votecount = getVotecount(1, page2, URL, postNumber)
			print("Returned to bot: " + votecount + "_")
			await channel.send(votecount + "\n\nYou can view this votecount and all previous votecounts in the #votecounts channel in Discord.")
		# await updateStatus("$votecount help")


client.loop.create_task(checkForData())
client.run(TOKEN)
