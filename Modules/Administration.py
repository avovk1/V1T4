import discord
from discord.ext import commands
import json
import random

class Administration(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        with open("Data/administration.json", "rt") as file:
            self.data:dict = json.load(file)
        self.bot:commands.Bot = bot

    @commands.command(name = "configure")
    async def configure(self, ctx:commands.Context) -> None:
        pass

    @commands.Cog.listener("on_message")
    async def sticker_ban(self, ctx:commands.Context) -> None:
        pass
        #if ctx.message.stickers

def setup(bot:commands.Bot) -> None:
    bot.add_cog(Administration(bot))