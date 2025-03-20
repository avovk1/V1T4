import json
import random

import discord
from discord.ext import commands

class Interactions(commands.Cog):
    """This cog is designed to fasilitate text-to-GIF, mainly expressing actions.
    Why am I doing this shit?
    """
    
    def __init__(self, bot:commands.Bot) -> None:
        # ToDo: migration towards SQLite, since json is not a DB
        # Kinda ironic from me, whom always said that "JSON is my DB"
        with open("Data/interactions.json", "rt") as file:
            self.data:dict = json.load(file)
        self.bot:commands.Bot = bot

    @commands.command(name = "configure")
    async def configure(self, ctx:commands.Context) -> None:
        """General configuration function for this module.
        Sets server-specific configuration, so this function requires server-specific configuration.
        """
        pass


def setup(bot:commands.Bot) -> None:
    bot.add_cog(Interactions(bot))