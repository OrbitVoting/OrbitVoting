# OrbitVoting


Summary: This is a script that calculates and creates votecounts.

What do I need to do to run this?

1) Download the latest version of the python 3 interpreter. Not python 2, but python 3.


2) Install --requirements:
Basically, the bot has some modules (extra programs) that are needed to run the program.

First, navigate to wherever you're keeping the project folder. Go to the command prompt, and navigate via the cd tool to the folder.

ex. C:/User/documents/orbitVoting

Then, type pip install --requirements

3) Get Google API credentials. Super easy: https://support.google.com/googleapi/answer/6158862, but rather than "API key", you want "OAuth Client ID". 

4) Download the provided .json file, make sure it's called "credentials.json", and stick them in the Orbit folder.

5) Run the app.py file.


Game specific info:

-You'll need a spreadsheet based on this template: LINK

-In main.py, set the spreadsheet ID to the id of the spreadsheet.

-In the app.py, set the pageURL variable to the desired page.
