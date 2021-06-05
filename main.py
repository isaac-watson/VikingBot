from asyncio.windows_events import NULL
import discord
from discord import voice_client
from discord.ext import commands
import json
import os
import random
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

cardArr = ["ClubsAce.png",
            "Clubs2.png",
            "Clubs3.png",
            "Clubs4.png",
            "Clubs5.png",
            "Clubs6.png",
            "Clubs7.png",
            "Clubs8.png",
            "Clubs9.png",
            "Clubs10.png",
            "ClubsJack.png",
            "ClubsQueen.png",
            "ClubsKing.png",
            "SpadesAce.png",
            "Spades2.png",
            "Spades3.png",
            "Spades4.png",
            "Spades5.png",
            "Spades6.png",
            "Spades7.png",
            "Spades8.png",
            "Spades9.png",
            "Spades10.png",
            "SpadesJack.png",
            "SpadesQueen.png",
            "SpadesKing.png",
            "HeartsAce.png",
            "Hearts2.png",
            "Hearts3.png",
            "Hearts4.png",
            "Hearts5.png",
            "Hearts6.png",
            "Hearts7.png",
            "Hearts8.png",
            "Hearts9.png",
            "Hearts10.png",
            "HeartsJack.png",
            "HeartsQueen.png",
            "HeartsKing.png",
            "DiamondsAce.png",
            "Diamonds2.png",
            "Diamonds3.png",
            "Diamonds4.png",
            "Diamonds5.png",
            "Diamonds6.png",
            "Diamonds7.png",
            "Diamonds8.png",
            "Diamonds9.png",
            "Diamonds10.png",
            "DiamondsJack.png",
            "DiamondsQueen.png",
            "DiamondsKing.png"]

class Player:

    cardsDrawn = []

    def __init__(self):
        self.hand = []
        self.bBust = False
        self.bBlkJak = False
        self.bStay = False
        self.val = [0,0] 


    def randomCard(self):
        rnum = random.randint(0,51)
        if cardArr[rnum] in self.cardsDrawn:
            self.randomCard()
        else:
            self.hand.append(cardArr[rnum])
            self.__cardValue(cardArr[rnum])
            self.cardsDrawn.append(cardArr[rnum])

    def updateStay(self):
        self.bStay = True
    
    
    def __cardValue(self, card):
        if "Ace" in card:
            self.val[0] += 1
            self.val[1] += 11
        elif "2" in card:
            self.val[0] += 2
            self.val[1] += 2
        elif "3" in card:
            self.val[0] += 3
            self.val[1] += 3
        elif "4" in card:
            self.val[0] += 4
            self.val[1] += 4
        elif "5" in card:
            self.val[0] += 5
            self.val[1] += 5
        elif "6" in card:
            self.val[0] += 6
            self.val[1] += 6
        elif "7" in card:
            self.val[0] += 7
            self.val[1] += 7
        elif "8" in card:
            self.val[0] += 8
            self.val[1] += 8
        elif "9" in card:
            self.val[0] += 9
            self.val[1] += 9
        else:
            self.val[0] += 10
            self.val[1] += 10

        if self.val[0] > 21 and self.val[1] > 21:
            self.bBust = True
        elif self.val[0] == 21 or self.val[1] == 21:
            self.bBlkJak = True


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
async def blackjack(ctx, *arg):
    p1 = Player()
    dealer = Player()

    p1.randomCard()
    dealer.randomCard()
    p1.randomCard()
    dealer.randomCard()

    startGame(p1, dealer)
    await ctx.send(file=discord.File('Content/gamestate.png'))

    while (p1.bBlkJak == False and p1.bBust == False and p1.bStay == False):
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        if reaction.emoji.name == 'sadge':
            p1.randomCard()
            updateGame(p1, dealer, "p1")
            await ctx.send(file=discord.File('Content/gamestate.png'))
        elif reaction.emoji.name == 'mattPoggers':
            p1.updateStay()

    while(dealer.bBlkJak == False and dealer.bBust == False and dealer.val[0] < 17 and p1.bBust != True):
        dealer.randomCard()
        updateGame(p1, dealer, "dealer")
        await ctx.send(file=discord.File('Content/gamestate.png'))
        time.sleep(5)



    
def startGame(p1, dealer):
    im = Image.new('RGBA',(500,500), (0,0,0,1))

    for card in p1.hand:
        im2 = Image.open('Content/Cards/' + card)
        Y = 386 - (p1.hand.index(card) * 15)
        X = p1.hand.index(card) * 15
        im.paste(im2.copy(), (X, Y))
        im2.close()


    for card in dealer.hand:
        im2 = Image.open('Content/Cards/' + card)
        Y = 25
        X = 175 + dealer.hand.index(card) * 81
        im.paste(im2.copy(), (X, Y))
        im2.close()
    
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Content/alata-regular.ttf", 16)
    draw.text((225, 0),"Dealer",(255,255,255),font=font)
    draw.text((10, 480),"Player 1",(255,255,255),font=font)
    im.save("Content/gamestate.png")
    im.close()

def updateGame(p1, dealer, who):
    im = Image.open('Content/gamestate.png')
    if who == "p1":
        adjust = (len(p1.hand) - 1)
        card = p1.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 386 - (adjust  * 15)
        X = adjust * 15
        im.paste(im2.copy(), (X, Y))
    else:
        adjust = (len(dealer.hand) - 1)
        card = dealer.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 25
        X = 175 + dealer.hand.index(card) * 81
        im.paste(im2.copy(), (X, Y))

       

    im.save("Content/gamestate.png")
    im2.close()


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
        voice_client.play(discord.FFmpegPCMAudio('Content/text.mp3'), after= await leaveChat(ctx) )


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