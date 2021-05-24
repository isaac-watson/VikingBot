from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import json
import os
from google.cloud.speech_v1.types.cloud_speech import RecognizeResponse
import pyaudio
import time
from google.cloud import speech
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#credentials = service_account.Credentials.from_service_account_file('GoogleCredentials.json')
client = speech.SpeechClient.from_service_account_json('GoogleCredentials.json')

r = sr.Recognizer()
CHUNK=2048
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000

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

                p = pyaudio.PyAudio()
                stream=p.open(
                    format=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK
                )

                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    audio_channel_count=1,
                    sample_rate_hertz=16000,
                    language_code="en-US"
                )

                t_end = time.time() + 10

                while time.time() < t_end:
                    try:
                        data=stream.read(CHUNK)
                        ctx.voice_client.send_audio_packet(data, encode=False)
                        print(data)
                    except:
                        print("failed to send audio packet")

                
                audio = speech.RecognitionAudio(content=data) 
                response = client.recognize(config=config, audio=audio)

                for result in response.results:
                    print("Transcript: {}".format(result.alternatives[0].transcript))

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