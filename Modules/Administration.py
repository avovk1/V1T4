import discord
from discord.ext import commands
import json
import random

class Administration(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        with open("Data/administration.json", "rt") as file:
            self.data = json.load(file)
        self.bot:commands.bot = bot

    @commands.command(name = "configure")
    async def configure(self) -> None:
        pass


def setup(bot) -> None:
    bot.add_cog(Administration(bot))