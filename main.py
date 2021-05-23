from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import json
import os
import speech_recognition as SR
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GTOKEN = os.getenv("GOOLE_API")

bot = commands.Bot(command_prefix="$", description="A bot")


channel_dict = {
    'bot-voice': 845413017473515551,
    'general' : 398673802537598977,
    'general2' : 754202862959067236,
    'waiting_room': 468587294450778114,
    'quarantine' : 388179281446174721
    }


@bot.event
async def on_ready():
    print('We have logged in as ' + (bot.user.name))
    global emotes
    emotes = bot.emojis
    
@bot.command()
async def ping(ctx, arg):
    await ctx.send(arg)  

@bot.command()
async def summon(ctx, *args):
    if (args != ()):
        try:
            if (ctx.voice_client is None):
                channel = bot.get_channel(channel_dict[args[0]])
                await channel.connect()
            else:
                await ctx.voice_client.disconnect()
                channel = bot.get_channel(channel_dict[args[0]])
                await channel.connect()

        except:
            await ctx.send("Channel does not exist or I'm banned " + find_emote(':sadge:'))
    else:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.send("I'm banned" + find_emote(':sadge:'))

@bot.command()
async def banish(ctx):
    await ctx.voice_client.disconnect()

def find_emote(name):
    for emote in emotes:
        if (str(emote).find(name) != -1):
            return str(emote)        

bot.run(TOKEN)