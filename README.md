This is a Discord bot, that gets and displays information about a Minecraft Server, using the Minecraft Server Status API (https://api.mcsrvstat.us/).
By default it updates it's information every minute, but you may change this in envs.json (more information below).
In it's status it displays the IP of the server and the current number of players, if the server is online. Otherwise, it will say that the server is offline.
Everytime a change in player count is detected, it will send an update message in a specified channel.
The update message contains the IP of the server, online status, and a list of players currently online.

HOW TO USE
---
In Discord, go to your User Settings, select "Advanced" and enable "Developer Mode"
Open a web browser of your choice and go to https://discord.com/developers/applications. 
Click the "New Application" button in the upper right corner, enter a Name (any will do), click the checkmark and choose "Create".
Navigate to the "Bot" section in the menu on the left side, then click the "Add Bot" button and confirm.
Choose "Reset Token", follow the steps and copy the new one to the "TOKEN" field in env.json
Scroll down to "Bot Permissions" and choose the following: "Send Messages", "Manage Messages" and "Read Message History".
After that, in the menu on the lefthand side, open the "OAuth2" section and go to "URL Generator".
For "Scopes" choose "bot", then for "Bot Permissions" select the same ones as earlier.
Then open the link at the bottom in your browser.
Choose a Server to add it to from the dropdown menu, and that part is done.

env.json
---
**TOKEN**

As mentioned earlier, "TOKEN" is where you put the token of the discord bot.

**CHANNEL_ID**

This is for specifying which channel the update messages should get sent to. 
You can get the ID of a channel by right clicking it and selecting "Copy ID", if you have Developer Mode enabled.

**SERVER_ID**

Same as CHANNEL_ID, but replace "channel" with "server".

**IP**

This is for specifying the IP which the server runs on.
If you plan to run this on the same machine or network as the server, you may leave it empty and the bot will autodetect your external IP.
If your external IP changes, while the server is running, it will try to detect your new one.
This also means that you can use it to keep the people playing on your server updated with your current IP, if you have a dynamic one.

**DELETE_MESSAGES**

By default, every time the bot sends a Status Update, it will check the last 100 messages in the channel, and delete any that have been sent by it.
This is to prevent flooding of a channel with Status Updates.
You may change the number of messages it looks through, or disable it entirely by setting the variable to 0.

**DELAY_MINS**

This variable is for specifying how many minutes the bot should wait before updating it's information again.
Setting it lower than 5 isn't recommended as the API will cache data for that amount of time.

Final Steps
---
Make sure you have python 3 installed, if not, install it.
Run the following commands to install python libraries:
pip install discord.py
pip install requests
Then, put bot.py and env.json in any directory, just make sure they're in the same one.
Finally, run bot.py with "python3 bot.py" (or some other way of running a python script) and you're done.
