from discord.ext import tasks
import discord
from discord.ext import commands
from requests import get
from json import loads
from json import load

#loading env.json
f = open('env.json')
envs = load(f)

#setting the bot token
TOKEN = envs['TOKEN']
#setting IP to the one provided in env.json
IP = envs['IP']
#if none has been provided, setting IP to the external IP of the machine this runs on
if IP == "":
    IP = get('https://api.ipify.org').content.decode('utf8')
#making global variables for the value of players for the current and previous loop
LAST_PLAYERS = "0"
CURRENT_PLAYERS = "0"
#variables to store contents of env.json so that it can be closed later
SERVER_ID = envs['SERVER_ID']
CHANNEL_ID = envs['CHANNEL_ID']
DELETE_MESSAGES = envs['DELETE_MESSAGES']
DELAY_MINS = envs['DELAY_MINS']
IP_provided = (envs['IP'] != "")

#initializing discord client
client = discord.Client(intents=discord.Intents.default())

#making the code loop every minute
@tasks.loop(minutes=DELAY_MINS)
async def get_server_info():
    #making the global variables writable
    global LAST_PLAYERS
    global CURRENT_PLAYERS
    global IP
    #settign LAST_PLAYERS to the
    LAST_PLAYERS = CURRENT_PLAYERS
    #fetching guild (server) and channel
    guild = await client.fetch_guild(SERVER_ID)
    channel = await guild.fetch_channel(CHANNEL_ID)
    #makes a request to the API
    server_data = loads(get("https://api.mcsrvstat.us/2/" + IP).text)
    #pre-emptively sets the status to offline
    online_string = "offline"
    #check if the API returns, that the server is online
    if server_data['online']:
        #if it is, get number of players and add them to the string. Also change offline to online.
        CURRENT_PLAYERS = str(server_data['players']['online'])
        online_string = CURRENT_PLAYERS + " players online"
    #check if there's been a change in player count
    if(int(CURRENT_PLAYERS) != int(LAST_PLAYERS)):
        #check if messages should be deleted
        if DELETE_MESSAGES > 0:
            #check if there have been any previous messages sent by the bot within the past x messages
            async for message in channel.history(limit=DELETE_MESSAGES):
                #check if message author is the bot
                if message.author == client.user:
                    #if yes, delete the message
                    await message.delete()
        #check if API returned offline
        if online_string != "offline":
            #if not, work on the online Status Update
            message = "```\nServer Status Update:\nIP: " + IP + " | \U0001F7E2 Online\n"
            #check if there is at least one player online
            if server_data['players']['online'] > 0:
                message += "Current Players:"
                #add all player names to the Update
                for player in server_data['players']['list']:
                    message += "\n-) " + player
                message += "\n```"
            #if no one is online, change message accordingly
            else:
                message += "No Players Currently Online\n```"
            #send the Update
            await channel.send(message)
        #do this if the API returns offline
        else:
            #send offline Status Update
            await channel.send("```\nServer Status Update:\nIP: " + IP + " | \U0001F534 Offline\n```")
    #check if server is offline
    if online_string == "offline":
        #in case this was caused by a change in IP, get external IP again, if none has been provided
        if not IP_provided:
            IP = get('https://api.ipify.org').content.decode('utf8')
    #change Bot status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=IP + " | " + online_string))

#define function that executes once after the bot starts
@client.event
async def on_ready():
    await client.wait_until_ready()
    #run the looping function
    get_server_info.start()

#closing env.json
f.close()

#run bot
client.run(TOKEN)
