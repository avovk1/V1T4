import discord
from discord.ext import commands
import json
import random

class Interactions(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        with open("Data/interactions.json", "rt") as file:
            self.data:dict = json.load(file)
        self.bot:commands.Bot = bot

    @commands.command(name = "configure")
    async def configure(self, ctx:commands.Context) -> None:
        pass


def setup(bot:commands.Bot) -> None:
    bot.add_cog(Interactions(bot))