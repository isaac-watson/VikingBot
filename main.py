import discord
import json
import os

from discord import user
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='$')

bot.pred_open = False
bot.can_bet = False
bot.pred = ""
bot.choice1 = ""
bot.choice2 = ""

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def commands(ctx, arg=None):
    commands_list = ['bank', 'openpred']
    if arg is None:
        await ctx.send("List of commands:\n\n*::bank*\n*::openpred \"Prediction text\"*\n\n"
                       "You can also do *::commands* **command name** for info on "
                       "the syntax of the specified command.")
    else:
        for c in commands_list:
            if arg == c:
                if c == 'bank':
                    await ctx.send(f"Do you really need syntactical help with this command, {ctx.author.name}?")
                if c == 'openpred':
                    await ctx.send("ok")
                break
            elif commands_list.index(c) == len(commands_list) - 1:
                await ctx.send("Error: No info on the command: *::{}*".format(arg))


@bot.command()
async def openpred(ctx, *, arg):
    if bot.pred_open:
        await ctx.send("There is already a prediction open. You can only open one at a time.")
    else:
        await ctx.send("Prediction opened! Place your bets...\n\n" + arg)
        bot.pred_open = True
        bot.can_bet = True
        bot.pred = arg

@bot.command()
async def choice1(ctx, *, arg):
    pass

@bot.command()
async def choice2(ctx, *, arg):
    pass

@bot.command()
async def bet(ctx, arg1, arg2):
    if bot.can_bet:
        return
    else:
        await ctx.send('Betting for this prediction is closed, you missed your chance!')

@bot.command()
async def closebets(ctx):
    bot.can_bet = False

@bot.command()
async def resetpred(ctx):
    bot.pred_open = False
    bot.can_bet = False
    bot.pred = ""
    bot.choice1 = ""
    bot.choice2 = ""
    ctx.send('Prediction has been reset. Ready to start a new one...≈')

@bot.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

    user_id = str(message.author.id)

    if message.author == bot.user:
        return
    else:
        await update_data(users, user_id)

    if message.author.display_name == "OrnateGale":
        emoji = bot.get_emoji(718618579918127124)
        await message.add_reaction(emoji)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('::bank'):
        await message.channel.send('You have ' + '${:,}'.format((users[user_id]["money"])))

    with open("users.json", "w") as f:
        json.dump(users, f)

    await bot.process_commands(message)


async def update_data(users, user_id):
    if not user_id in users:
        users[user_id] = {}
        users[user_id]["money"] = 0


bot.run(TOKEN)
