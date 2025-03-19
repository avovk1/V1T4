import discord
from discord.ext import commands
import json
import random

class Interactions(commands.Cog):
    def __init__(self, bot) -> None:
        with open("Data/interactions.json", "rt") as file:
            self.data = json.load(file)
        self.bot = bot

    @commands.command(name = "configure")
    async def configure(self) -> None:
        pass


def setup(bot) -> None:
    bot.add_cog(Interactions(bot))