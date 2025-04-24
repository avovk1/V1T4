import json
#import sqlite3

# import discord
from discord.ext import commands

class Administration(commands.Cog):
    """
    This cog is designed to do the heavy-lifting on all administrative roles V1T4 should perform
    """

    def __init__(self, bot:commands.Bot) -> None:
        # ToDo: migration towards SQLite, since json is not a DB
        # Kinda ironic from me, whom always said that "JSON is my DB"
        with open("Data/administration.json", "rt", encoding = "UTF-8") as file:
            self.data:dict = json.load(file)
        self.bot:commands.Bot = bot

    def cog_unload(self) -> None:
        print("goodbye world!")

    # @commands.command(name = "configure")
    # async def configure(self, ctx:commands.Context) -> None:
    #     """General configuration function for this module.
    #     Sets server-specific configuration
    #     so this function requires server-specific configuration
    #     """
    #     pass

    # @commands.Cog.listener("on_message")
    # async def sticker_ban(self, ctx:commands.Context) -> None:
    #     """Bans users if they get replied with required sticker.
    #     Normally turned off.
    #     Required stickers are dependent on server,
    #     thus this function requires server-specific configuration.
    #     """
    #     pass

def setup(bot:commands.Bot) -> None:
    """boilerplate"""
    bot.add_cog(Administration(bot))
