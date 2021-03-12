import os
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from bitcoinbot.bitcoin import Bitcoin
from bitcoinbot.httpservice import HttpService

class BitcoinBot(commands.Cog):
    def __init__(self, bot):
        self.bitcoin = Bitcoin()
        self.http = HttpService()
        self.bot = bot
        self.channels = {}
        self.loadChannels()
        self.checkPrice.start()

    def loadChannels(self):
        with open("ressources/channels.json") as channel_file:
            try:
                self.channels = json.load(channel_file)
            except json.decoder.JSONDecodeError:
                pass

    def saveChannels(self):
        with open('ressources/channels.json', 'w') as channel_file:
            json.dump(self.channels, channel_file)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.channels:
            if type(channel) is discord.channel.TextChannel and channel.name == 'general':
                self.channels[guild.id] = channel.id
                await channel.send(f"Successfully initialized ``{channel.name}`` "
                                   f"with id: ``{self.channels[guild.id]}``")
        #Case no general channel pick first channel
        if self.channels[guild.id] == None:
            self.channels[guild.id] = guild.channels[0].id
            await guild.channels[0].send(f"Successfully initialized ``{guild.channels[0].name}`` "
                               f"with id: ``{self.channels[guild.id]}``")
        self.saveChannels()

    @commands.command(name='initChannel')
    async def initChannel(self, ctx):
        self.channels[ctx.guild.id] = ctx.channel.id
        await self.sendInitMessage(ctx)
        self.saveChannels()

    @commands.command(name='bearish')
    async def bearish(self, ctx):
        price, _ = self.http.getPrice()
        if price != -1:
            response = self.bearishMessge(mark=self.bitcoin.prevMilestone, price=price)
        else:
            response = "Failed to fetch market data. Try again."

        await ctx.send(content=response, file=discord.File("ressources/bear.gif"))

    @commands.command(name='retesting')
    async def retesting(self, ctx):
        price, _ = self.http.getPrice()
        if price != -1:
            response = self.retestingMessage(mark=self.bitcoin.nextMilestone, price=price)
        else:
            response = "Failed to fetch market data. Try again."
        await ctx.send(content=response, file=discord.File("ressources/btcRetesting.jpg"))

    @commands.command(name='bullish')
    async def bullish(self, ctx):
        _, ath = self.http.getPrice()
        if ath != -1:
            response = self.bullishMessage(mark=self.bitcoin.nextMilestone, ath=ath)
        else:
            response = "Failed to fetch market data. Try again."
        await ctx.send(content=response, file=discord.File("ressources/bitcoinbullrun.gif"))

    @tasks.loop(minutes=15.0)
    async def checkPrice(self):
        price, ath = self.http.getPrice()
        if price != -1 and ath != -1:
            if price > self.bitcoin.nextMilestone and ath > self.bitcoin.ath:
                await self.sendBullishMessage(mark=self.bitcoin.nextMilestone, ath=ath)
                self.bitcoin.updateMilestones(bullish=True)
                self.bitcoin.updateATH(ath)
            elif price > self.bitcoin.nextMilestone:
                await self.sendRetestingMessage(mark=self.bitcoin.nextMilestone, price=price)
                self.bitcoin.updateMilestones(bullish=True)
            elif price < self.bitcoin.prevMilestone:
                await self.sendBearishMessage(mark=self.bitcoin.prevMilestone, price=price)
                self.bitcoin.updateMilestones(bullish=False)

    @checkPrice.before_loop
    async def before_checkPrice(self):
        await self.bot.wait_until_ready()

    async def sendInitMessage(self, ctx):
        await ctx.send(content=f"Successfully initialized ``{ctx.channel.name}`` with id: ``{self.channels[ctx.guild.id]}``")

    async def sendBullishMessage(self, mark, ath):
        for guild in self.bot.guilds:
            channel = guild.get_channel(self.channels[guild.id])
            if channel is not None:
                await channel.send(content=self.bullishMessage(mark=mark, ath=ath))
            else:
                #ToDo:log no channel found
                pass

    async def sendRetestingMessage(self, mark, price):
        for guild in self.bot.guilds:
            channel = guild.get_channel(self.channels[guild.id])
            if channel is not None:
                await channel.send(content=self.retestingMessage(mark=mark, price=price))
            else:
                #ToDo:log no channel found
                pass

    async def sendBearishMessage(self, mark, price):
        for guild in self.bot.guilds:
            channel = guild.get_channel(self.channels[guild.id])
            if channel is not None:
                await channel.send(content=self.bearishMessage(mark=mark, price=price))
            else:
                #ToDo:log no channel found
                pass

    def bullishMessage(self, mark, ath):
        return f':rocket: Bitcoin passed the ${mark} mark for the first time ever, reaching a new all-time high of ${ath}! :rocket:'

    def retestingMessage(self, mark, price):
        return f'Bitcoin successfully retested the ${mark} mark! Currently worth ${price}.'

    def bearishMessge(self, mark, price):
        return f'Bitcoin fell back under the previous ${mark} mark and is currently worth ${price}. HODL brothers, Diamond hands only!'


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')
bot.add_cog(BitcoinBot(bot))
bot.run(TOKEN)