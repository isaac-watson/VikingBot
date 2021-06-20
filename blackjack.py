import time
import random
import discord
import json
from asyncio.windows_events import NULL
from PIL import Image, ImageDraw, ImageFont
from discord.ext.commands.converter import GameConverter

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

game_controls = {
    "hit"        : "🔽",
    "stay"       : "⏸",
    "doubledown" : "⏬",
    "quit"       : "⏹",
    "playagain"  : "🔁",
    "join"       : "▶",
    "continue"   : "✅",
    "checkbank"  : "🏧",
    25           : "⚪",
    50           : "🔵",
    100          : "🟤",
    200          : "🟢",
    500          : "🟣",
    1000         : "🟡",
    2000         : "🟠",
    5000         : "🔴",
    10000        : "⚫",
    0.5          : "⬜",
    0.0          : "⬛",
}

class Player:
    
    cardsDrawn = []

    def __init__(self):
        self.hand = []
        self.bBust = False
        self.bBlkJak = False
        self.bStay = False
        self.val = 0
        self.bet = 0
        self.userid = ""


    def randomCard(self):
        rnum = random.randint(0,51)
        if cardArr[rnum] in self.cardsDrawn:
            self.randomCard()
        else:
            self.hand.append(cardArr[rnum])
            self.__cardValue(self.hand)
            self.cardsDrawn.append(cardArr[rnum])

    def updateStay(self):
        self.bStay = True
    
    
    def __cardValue(self, hand):
        self.val = 0
        aces = 0
        for card in hand:
            if "Ace" in card:
                aces += 1
                self.val += 11
            elif "2" in card:
                self.val += 2
            elif "3" in card:
                self.val += 3
            elif "4" in card:
                self.val += 4
            elif "5" in card:
                self.val += 5
            elif "6" in card:
                self.val += 6
            elif "7" in card:
                self.val += 7
            elif "8" in card:
                self.val += 8
            elif "9" in card:
                self.val += 9
            else:
                self.val += 10
        
        while aces > 0 and self.val > 21:
            self.val -= 10
            aces -= 1

        if self.val > 21:
            self.bBust = True
        elif self.val == 21:
            self.bBlkJak = True

async def startGame(bot, ctx, arg):
    im = Image.new('RGBA',(500,500), (0,0,0,1))
    p  = []
    i = int(arg)

    while i > 0:
        p.append(Player())
        i -=1
    
    if p == []:
        p.append(Player())

    if len(p) != 1:
        msg = await ctx.send("If you would like to join the game press the ▶ button (exculding " + str(ctx.author.name) + ")")
        await msg.add_reaction(game_controls["join"])
        await msg.add_reaction(game_controls["continue"])
        p[0].userid = str(ctx.author.id)

        i = 1
        while p[len(p) - 1].userid  == "":
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0)

            if reaction.emoji == game_controls["join"] and user.bot == False and str(user.id) != p[0].userid:
                p[i].userid = str(user.id)
                i += 1
            elif reaction.emoji == game_controls["continue"] and user.bot == False:
                rm = []
                for player in p:
                    if player.userid == "":
                        rm.append(p.index(player))

                rm.reverse()

                for index in rm:
                    del p[index]

                break

    dealer = Player()

    with open("users.json", "r") as f:
        users = json.load(f)

    msg = await ctx.send("""To place a bet refer to this table:
                    \n⚪ = $25
                    \n🔵 = $50
                    \n🟤 = $100
                    \n🟢 = $200
                    \n🟣 = $500
                    \n🟡 = $1000
                    \n🟠 = $2000
                    \n🔴 = $5000
                    \n⚫ = $10000
                    \n⬜ = 50% of bank
                    \n⬛ = 100% of bank
                    \n🏧   to check bank\n\n""")

    

    for key in game_controls:
        if (type(key) == float or type(key) == int):
            await msg.add_reaction(game_controls[key])

    await msg.add_reaction(game_controls["checkbank"])
    
    while True:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        i = 0
        if reaction.emoji == "🏧" and user.bot == False:
            await ctx.send(user.name + "'s Current Bank: $ " + str(users[str(user.id)]["money"]))
        elif (user.bot == False): 
            for player in p:
                if str(user.id) == player.userid:
                    player.bet = get_key(reaction.emoji)
                    player.bet = place_bet(player.bet, user)
            
            for player in p:
                if player.bet != 0:
                    i += 1

            if i >= len(p):
                break
    
    hidden_card = firstHand(p, dealer, im)

    msg = await ctx.send(file=discord.File('Content/gamestate.png'))
    await printControls(msg)


    #Main black jack player loop, allows the player to hit, stay or double down until they bust
    for player in p:
        while (player.bBlkJak == False and player.bBust == False and player.bStay == False):
            try:
                await ctx.send("Player " + str(p.index(player) + 1) +  " Turn")
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0)

                if user.bot == False and str(user.id) == player.userid:
                    if reaction.emoji == game_controls["hit"]:
                        hit(player, dealer, p.index(player))
                        await msg.delete()
                        msg = await ctx.send(file=discord.File('Content/gamestate.png'))
                        await printControls(msg)
                    elif reaction.emoji == game_controls["stay"]:
                        stay(player)
                    elif reaction.emoji == game_controls["doubledown"]:
                        temp = player.bet
                        player.bet = place_bet(player.bet, user)
                        hit(player, dealer, p.index(player))
                        await msg.delete()
                        msg = await ctx.send(file=discord.File('Content/gamestate.png'))
                        player.bet += temp + player.bet
                        stay(player)
                elif user.bot == False and str(user.id) != player.userid:
                     await ctx.send("You are not player " + str(p.index(player) + 1))
            except:
                stay(player)
    
    #Reveal hidden card and place it over hidden card
    await msg.delete()
    im = Image.open('Content/gamestate.png')
    im2 = Image.open('Content/Cards/' + hidden_card)
    Y = 25
    X = 81
    im.paste(im2.copy(), (X, Y))
    im.save("Content/gamestate.png")
    im.close()
    im2.close()
    msg = await ctx.send(file=discord.File('Content/gamestate.png'))
    time.sleep(3)

    #Main dealer loop, the dealer draws to 17 minimum or until they bust
    while(dealer.bBlkJak == False and dealer.bBust == False and dealer.val < 17 ):
        hit(p[0], dealer, "dealer")
        await msg.delete()
        msg = await ctx.send(file=discord.File('Content/gamestate.png'))
        time.sleep(5)


    #determine whether or not you won your bet and what they pay out will be
    for player in p:
        if ((player.bBlkJak == True and dealer.bBlkJak != False) or 
            (player.val > dealer.val and player.bBust == False) or (dealer.bBust == True and player.bBust == False)):
            await winnings(player.bet, user, ctx)
        elif player.val == dealer.val:
            player.bet /= 2
            await winnings(player.bet, user, ctx)
        else:
            player.bet = 0
            await winnings(player.bet, user, ctx)
    


    await msg.add_reaction(game_controls["playagain"])
    await msg.add_reaction(game_controls["quit"])

    p[0].cardsDrawn = []

    try:
        while True:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
            if reaction.emoji == game_controls["playagain"] and user.bot == False:
                await startGame(bot, ctx)
                break
            elif reaction.emoji == game_controls["quit"] and user.bot == False:
                await ctx.send("Thanks for Playing")
                break
    except:
        await ctx.send("Thanks for Playing")

def hit(p, dealer, who):
    im = Image.open('Content/gamestate.png')

    if who != "dealer":
        p.randomCard()
        adjust = (len(p.hand) - 1)
        card = p.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 386 - (adjust  * 15)
        X = who * 121 + adjust * 15
        im.paste(im2.copy(), (X, Y))
    else:
        dealer.randomCard()
        adjust = (len(dealer.hand) - 1)
        card = dealer.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 25
        X = dealer.hand.index(card) * 81
        im.paste(im2.copy(), (X, Y))

    im.save("Content/gamestate.png")
    im.close()
    im2.close()

def stay(player):
    player.updateStay()

async def printControls(msg):
    await msg.add_reaction(game_controls["hit"])
    await msg.add_reaction(game_controls["stay"])
    await msg.add_reaction(game_controls["doubledown"])

def firstHand(p, dealer, im):

    for player in p:
        player.randomCard()

    dealer.randomCard()

    for player in p:
        player.randomCard()

    dealer.randomCard()
    hidden_card = dealer.hand[1]

    for player in p:
        for card in player.hand:
            im2 = Image.open('Content/Cards/' + card)
            Y = 386 - (player.hand.index(card) * 15)
            X = p.index(player) * 121 + player.hand.index(card) * 15
            im.paste(im2.copy(), (X, Y))
            im2.close()

    im2 = Image.open('Content/Cards/' + card)
    Y = 25
    X = 0
    im.paste(im2.copy(), (X, Y))
    im2.close()

    im2 = Image.open('Content/Cards/HiddenCard.png')
    Y = 25
    X = 81
    im.paste(im2.copy(), (X, Y))
    im2.close()

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("Content/alata-regular.ttf", 16)
    draw.text((0, 0),"Dealer",(255,255,255),font=font)
    
    for player in p:
        draw.text((10 + p.index(player) * 121, 480),"Player " + str(p.index(player) + 1),(255,255,255),font=font)

    im.save("Content/gamestate.png")
    im.close()

    return hidden_card

def get_key(val):
    for key, value in game_controls.items():
         if val == value:
             return key

def place_bet(bet, user):
    with open("users.json", "r") as f:
        users = json.load(f)

    with open("users.json", "w") as f:
        user_id = str(user.id)
        if (type(bet) == int):
            if (users[user_id]["money"] >= bet):
                users[user_id]["money"] = users[user_id]["money"] - bet
            else:
                bet = users[user_id]["money"]
                users[user_id]["money"] = 0
        else:
            if bet == 0.0:
                bet = users[user_id]["money"]
                users[user_id]["money"] = 0
            else:
                bet = users[user_id]["money"] / 2
                users[user_id]["money"] = users[user_id]["money"] / 2
        
        json.dump(users, f)
    
    return bet

async def winnings(bet, user, ctx):
    with open("users.json", "r") as f:
        users = json.load(f)

    with open("users.json", "w") as f:
        user_id = str(user.id)
        users[user_id]["money"] += (bet * 2)
        await ctx.send('Current Bank: $' + str(users[user_id]["money"]))
        json.dump(users, f)