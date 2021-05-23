import discord
from discord.ext import commands
import json
import os
import speech_recognition as SR
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

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
    
@bot.command()
async def ping(ctx, arg):
    await ctx.send(arg)    

@bot.command()
async def summon(ctx, *args):
    if (args != ''):
        try:
            channel = bot.get_channel(channel_dict[args])
            await channel.connect()
        except:
            ctx.send("Channel does not exist or I'm banned :sadge:")
    else:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            ctx.send("I'm banned :sadge:")

@bot.command()
async def banish(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)