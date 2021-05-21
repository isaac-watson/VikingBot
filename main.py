import discord
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

    user_id = str(message.author.id)

    if message.author == client.user:
        return
    else:
        await update_data(users, user_id)

    if message.author.display_name == "OrnateGale":
        emoji = client.get_emoji(718618579918127124)
        await message.add_reaction(emoji)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('::bank'):
        await message.channel.send('You have ' + '${:,}'.format((users[user_id]["money"])))

    
    pred_open = False
    if message.content.startswith('::openpred'):
        if pred_open:
            await message.channel.send('There is already a prediction open. You can only open one at a time.')
        elif not pred_open:
            pred_open = True
            await message.channel.send('Prediction open. Place your bets')

    with open("users.json", "w") as f:
        json.dump(users, f)


async def update_data(users, user_id):
    if not user_id in users:
        users[user_id] = {}
        users[user_id]["money"] = 0


client.run(TOKEN)
