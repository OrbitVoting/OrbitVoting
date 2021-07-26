# Votecount Bot
A votecount bot created by Mark

## Overview
This is a simple discord bot that:
   - generates votecounts on demand
   - automatically generates votecounts every time interval and posts them in the #votecounts channel
   - Produces a list of living players and compares it to votecounts to generate a list of players are are not actively voting
   
## Commands
Note that, for now, all commands must be entered in the #votecounts channel in a discord server where the bot is added. The bot can process one votecount at a time and does not respond to commands while processing a votecount.

List of commands:
  - `$votecount help` - produces a handy list of commands and a brief description of what they do.
  - `$votecount url` - sets the url of the current game you want a votecount for. (Doesn't matter from which page the url comes from; the bot "cleans" the url)
  - `$votecount host <host name>` - sets the forum name of the game host. The host's votes do not count. This is to allow the host to post example votes (ex. [vote]Example[/vote] without the bot counting "Example" as a player. This command is case sensitive.
  - `$votecount <first page> <last page>` - generates a single votecount, starting on page <first page>, ending on page <last page>. Note that if the previous day ends on the same page as the current day, some of yesterday's votes will be counted, since the bot can't detect where on the page the current day started. To avoid this issue, allow a bit of banter to ensure day N starts on a page page that day N-1 ended.
  
  Handy tip: the bot can take a few minutes to generate the votecount (Approx. 4 seconds per page), and while doing so, sometimes players will post and start a new page on the thread. When using this command, it's recommended to make <last page> a number a bit greater than the current number of pages on the thread, to give a bit of buffer room in case people start a new page.
  
  Example: suppose Day N started on page 50 and the thread is currently at page 150. You would enter the command `$votecount 50 152` . The bot would start on page 50, and check every page until it gets to page 152. (And if page 152 does not exist, the bot will automatically stop wherever the thread ended)
  - `$votecount auto on <first page>` - turns on the automatic votecount feature. The bot will start at page <first page> and count votes until it gets to the end of the thread, then post the votecount.
  - `$votecount auto delay <minutes>` - sets the interval between votecounts. To be nice to the website (and to not flood the channel with identical votecounts) it's recommended to keep this to 120 minutes or more. Smaller increments (ex. 10, 30, or 60 minutes) may be necessary towards EoD.
  
  Note that the automatic votecounts will stop after 48 hours and will need to be reativated by command.
  - `$votecount auto off` - turns the automatic votecounts off. The bot will automatically trigger this command after 48 hours of continuous automatic votecounts.
  - `$votecount info` - prints the information saved on the server, including recent error messages (Useful for debugging)
## Mod-specific notes
- The votecount automatically scrapes the player list. To make this possible, you must:
  - have a spoiler titled "living players" that contains the list of players, where each player name is a valid @tag.
  - the living players spoiler must be immediately followed by a spoiler titled "dead players"
- The bot automatically scrapes the cycle # (Ex. Day 1, Night 4) from the thread title and prints this along with the votecount. If you are sloppy at updating the thread title, it may confuse players when the bot prints a votecount for Day 4 with the title "Day/Night 3 votecount."
   
 ## Other notes
 - Sometimes, the bot doesn't work. Usually, the problem goes away (ex. there was a website glitch). Sometimes, the website's DDoS protection kicks in; in previous times, these go away within a few days. There's a few things I can do to get around them, but not much.
 - If anyone wants to try to edit/fork/mess around with the code, that's chill - all files are here except for a file titled tokens.json and googleKey.json - these contain API key for the discord bot and the server I'm using to store data. You'll need to generate your own, which is easy.

   
   
  Written in Python
