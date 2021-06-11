
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
        
        while aces > 0:
            if self.val <= 10:
                self.val += 11
            else:
                self.val += 1
            
            aces -= 1

        if self.val > 21:
            self.bBust = True
        elif self.val == 21:
            self.bBlkJak = True

async def startGame(bot, ctx):
    im = Image.new('RGBA',(500,500), (0,0,0,1))
    p1 = Player()
    dealer = Player()

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
                    \n⬛ = 100% of bank\n\n"""
                   )

    for key in game_controls:
        if (type(key) == float or type(key) == int):
            await msg.add_reaction(game_controls[key])
    
    while True:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        if (user.bot == False): 
            bet = get_key(reaction.emoji)
            break
    
    bet = place_bet(bet, user)
    firstHand(p1, dealer, im)

    msg = await ctx.send(file=discord.File('Content/gamestate.png'))
    await printControls(msg)

    while (p1.bBlkJak == False and p1.bBust == False and p1.bStay == False):
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0)

            if reaction.emoji == game_controls["hit"] and user.bot == False:
                hit(p1, dealer, "p1")
                await msg.delete()
                msg = await ctx.send(file=discord.File('Content/gamestate.png'))
                await printControls(msg)
            elif reaction.emoji == game_controls["stay"] and user.bot == False:
                stay(p1)
            elif reaction.emoji == game_controls["doubledown"] and user.bot == False:
                place_bet(bet, user)
                hit(p1, dealer, "p1")
                bet += bet
                stay(p1)
        except:
            stay(p1)

    while(dealer.bBlkJak == False and dealer.bBust == False and dealer.val < 17 and p1.bBust != True):
        hit(p1, dealer, "dealer")
        await msg.delete()
        msg = await ctx.send(file=discord.File('Content/gamestate.png'))
        time.sleep(5)

    if ((p1.bBlkJak == True and dealer.bBlkJak != False) or 
        (p1.val > dealer.val and p1.bBust == False)):
        await winnings(bet, user, ctx)
    elif p1.val == dealer.val:
        bet /= 2
        await winnings(bet, user, ctx)
    else:
        bet = 0
        await winnings(bet, user, ctx)
    


    await msg.add_reaction(game_controls["playagain"])
    await msg.add_reaction(game_controls["quit"])

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

def hit(p1, dealer, who):
    im = Image.open('Content/gamestate.png')

    if who == "p1":
        p1.randomCard()
        adjust = (len(p1.hand) - 1)
        card = p1.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 386 - (adjust  * 15)
        X = adjust * 15
        im.paste(im2.copy(), (X, Y))
    else:
        dealer.randomCard()
        adjust = (len(dealer.hand) - 1)
        card = dealer.hand[adjust]

        im2 = Image.open('Content/Cards/' + card)
        Y = 25
        X = 175 + dealer.hand.index(card) * 81
        im.paste(im2.copy(), (X, Y))

    im.save("Content/gamestate.png")
    im2.close()

def stay(player):
    player.updateStay()

async def printControls(msg):
    await msg.add_reaction(game_controls["hit"])
    await msg.add_reaction(game_controls["stay"])
    await msg.add_reaction(game_controls["doubledown"])

def firstHand(p1, dealer, im):
    p1.randomCard()
    dealer.randomCard()
    p1.randomCard()
    dealer.randomCard()

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