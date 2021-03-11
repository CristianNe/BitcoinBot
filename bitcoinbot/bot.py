import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from bitcoinbot.bitcoin import Bitcoin
from bitcoinbot.httpservice import HttpService

class BitcoinBot(commands.Cog):
    def __int__(self, bot):
        self.bitcoin = Bitcoin()
        self.http = HttpService()
        self.bot = bot
        self.checkPrice.start()

    @commands.command(name='bearish')
    async def bearish(self, ctx):
        price, _ = await self.http.getPrice()
        if price != -1:
            response = self.bearishMessge(self.bitcoin.prevMilestone, price)
        else:
            response = "Failed to fetch market data. Try again."

        await ctx.send(content=response, file=discord.File("ressources/bear.gif"))

    @commands.command(name='bullish')
    async def bullish(self, ctx):
        _, ath = await self.http.getPrice()
        if ath != -1:
            response = self.bullishMessage(self.bitcoin.nextMilestone, ath)
        else:
            response = "Failed to fetch market data. Try again."
        await ctx.send(content=response, file=discord.File("ressources/bear.gif"))

    @tasks.loop(minutes=15.0)
    async def checkPrice(self):
        price, ath = self.http.getPrice()
        if price > self.bitcoin.nextMilestone and ath > self.bitcoin.ath:
            #send newATH message(mark=nextMilestone, newATH=price)
            self.bitcoin.updateMilestones(bullish=True)
            self.bitcoin.updateATH(ath)
        elif price > self.bitcoin.nextMilestone:
            #send retesting message (retest=nextMilestone)
            self.bitcoin.updateMilestones()
        elif price < self.bitcoin.prevMilestone:
            #send bullish message ()
            self.bitcoin.updateMilestones(bullish=False)

    @checkPrice.before_loop
    async def before_checkPrice(self):
        await self.bot.wait_until_ready()

    def bullishMessage(self, mark, ath):
        return f'Bitcoin passed the ${mark} mark for the first time ever, reaching a new all-time high of ${ath}!'

    def retestingMessage(self, mark, price):
        return f'Bitcoin successfully retested the ${mark} mark! Currently worth ${price}.'

    def bearishMessge(self, mark, price):
        return f'Bitcoin fell back under the previous ${mark} mark and is currently worth ${price}. HODL brothers, Diamond hands only!'


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')
bot.run(TOKEN)