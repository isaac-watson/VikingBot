from asyncio.windows_events import NULL
import discord
from discord import voice_client
from discord.ext import commands
import json
import os
import random
import blackjack
from PIL import Image, ImageDraw, ImageFont
from discord.flags import SystemChannelFlags
from gtts import gTTS
import time
from discord.ext.commands.core import command
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", description="A bot", intents=intents)


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
        await joinChat(ctx, args[0])
    else:
        await joinChat(ctx, ctx.author.voice.channel.name)


@bot.command()
async def banish(ctx):
    await leaveChat(ctx)


@bot.command()
async def insult(ctx, *args):     
    if (args == ()):
        #author = str(ctx.author)
        await ctx.send("Your an idiot " + ctx.message.author.mention)
    else:
        target = args[0]
        members = await getMembers(ctx)
        voiceMembers = getVoiceChatMembers(channel_dict['general'])
        
        if (target in voiceMembers):
            await joinChat(ctx, 'general')

            if ((target in members) and (len(args) != 2)):
                await speak(ctx.guild, (target + ' is Big Gay'), ctx)
            else:
                await speak(ctx.guild, args[1], ctx)
            
            voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            

            
            #await leaveChat(ctx)
        else:
            await ctx.send("Member not in chat " + findEmote(':PepeHands:'))

@bot.command()
async def talk(ctx, arg):
    if (ctx.author.voice.channel.name == 'General'):
        await joinChat(ctx, ctx.author.voice.channel.name)
        await speak(ctx.guild, arg, ctx)


@bot.command()
async def E (ctx):
    await ctx.send("EEEEEEEEEEEEEE\nE\nE\nE\nE\nE\nEEEEEEEEEEE\nE\nE\nE\nE\nE\nEEEEEEEEEEEEEE")

@bot.command()
async def BJ(ctx, *arg):
    await blackjack.startGame(bot, ctx)

async def getMembers(ctx):
    memberList = []

    async for member in ctx.guild.fetch_members(limit=None):
        memberList.append(member.name)
    
    return memberList

async def joinChat(ctx, channel):
    channel = channel.lower()
    try:
        if (channel in channel_dict) and (len(bot.voice_clients) == 0):
            vc = bot.get_channel(channel_dict[channel])
            await vc.connect()
        elif((channel in channel_dict) and (len(bot.voice_clients) > 0) and (bot.voice_clients[0].channel.id != channel_dict[channel])):
            await ctx.voice_client.disconnect()
            vc = bot.get_channel(channel_dict[channel])
            await vc.connect()
        else:
            await ctx.send("Channel does not exist or I'm already in channel moron" + findEmote(':ree:'))
    except:
        await ctx.send("I'm banned " + findEmote(':sadge:'))

async def leaveChat(ctx):
    await ctx.voice_client.disconnect()

async def speak(guild, msg, ctx):
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    tts = gTTS(msg)
    tts.save('Content/text.mp3')
    if not voice_client.is_playing():
        voice_client.play(discord.FFmpegPCMAudio('Content/text.mp3'), after= print('done') )


def getVoiceChatMembers(channel):
    activeMembers = bot.get_channel(channel)
    vcm = activeMembers.members
    members = [] 

    for member in vcm:
        members.append(member.name)

    return members

def findEmote(name):
    for emote in emotes:
        if (str(emote).find(name) != -1):
            return str(emote)

         


bot.run(TOKEN)