import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.command(name='bearish')
async def bearish(ctx):
    response = 'FUCK Bitcoin fell back under <price> :bearmarket:'

    await ctx.send(content=response, file=)
bot.run(TOKEN)