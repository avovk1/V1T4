import json
#import random

import discord
from discord.ext import commands

class Interactions(commands.Cog):
    """This cog is designed to fasilitate text-to-GIF, mainly expressing actions.
    Why am I doing this shit?
    """
    
    def __init__(self, bot:commands.Bot) -> None:
        # ToDo: migration towards SQLite, since json is not a DB
        # Kinda ironic from me, whom always said that "JSON is my DB"
        with open("Data/interactions.json", "rt", encoding = "UTF-8") as file:
            self.data:dict = json.load(file)
        self.bot:commands.Bot = bot

    def cog_unload(self) -> None:
        print("goodbye world!")
        
    class MyView(discord.ui.View):
        @discord.ui.button(label="Button 1", row=0, style=discord.ButtonStyle.primary)
        async def first_button_callback(self, button, interaction):
            await interaction.response.send_message("You pressed me!")

def setup(bot:commands.Bot) -> None:
    """boilerplate"""
    bot.add_cog(Interactions(bot))
