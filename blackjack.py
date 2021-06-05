
import time
import random
import discord
from asyncio.windows_events import NULL
from PIL import Image, ImageDraw, ImageFont

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

async def startGame(bot, ctx):
    im = Image.new('RGBA',(500,500), (0,0,0,1))
    p1 = Player()
    dealer = Player()

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
    
    await ctx.send(file=discord.File('Content/gamestate.png'))

    while (p1.bBlkJak == False and p1.bBust == False and p1.bStay == False):
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        if reaction.emoji.name == 'sadge':
            hit(p1, dealer, "p1")
            await ctx.send(file=discord.File('Content/gamestate.png'))
        elif reaction.emoji.name == 'mattPoggers':
            stay(p1)

    while(dealer.bBlkJak == False and dealer.bBust == False and dealer.val[0] < 17 and p1.bBust != True):
        hit(p1, dealer, "dealer")
        await ctx.send(file=discord.File('Content/gamestate.png'))
        time.sleep(5)

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

