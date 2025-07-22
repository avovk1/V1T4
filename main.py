"""Core of V1T4 bot"""

import sys
import json
from subprocess import Popen

import discord
from discord.ext import commands
from updater import check

DEBUG = False

try:
    with open("Data/token", "rt", encoding="UTF-8") as file:
        token = file.read() or ""
    if token == "":
        print("Token file is empty - provide actual token in ./Data/token file!")
        sys.exit(1)
except FileNotFoundError:
    if sys.stdin.isatty():
        token = input("File with token is empty, please enter valid token! > ")
        with open("Data/token", "wt", encoding="UTF-8") as file:
            file.write(token)
    else:
        token = "" # pylint: disable=C0103
        print("Token file is empty - provide actual token in ./Data/token file!")
        sys.exit(1)




with open("Data/config.json", "rt", encoding="UTF-8") as file:
    config = json.load(file)

with open("main_strings.json", "rt", encoding="UTF-8") as file:
    strings = json.load(file)

bot:commands.Bot = commands.Bot(command_prefix=config["prefix"],
                                intents = discord.Intents.all())

def cog_loader(name:str|None = None) -> str:
    """If provided with name - loads specific module.
    othervice loads all default
    """
    if name:
        string:str = ""
        if DEBUG:
            bot.load_extension("Modules."+name)
        else:
            try:
                bot.load_extension("Modules."+name)
                string = strings["load"]["success"]
            except discord.ExtensionNotFound:
                string = strings["load"]["notfound"]
            except discord.NoEntryPointError:
                string = strings["load"]["noentry"]
            except discord.ExtensionAlreadyLoaded:
                string = strings["load"]["loaded"]
            except discord.ExtensionFailed as error:
                string = strings["load"]["failure"] + str(error) + "\n"
            print(string.format(name = name))
        return string
    else:
        continuous_string:str = ""
        for i in config["modules"]:
            try:
                bot.load_extension("Modules."+i)
                string:str = strings["load"]["success"]
            except discord.ExtensionNotFound:
                string:str = strings["load"]["notfound"]
            except discord.NoEntryPointError:
                string:str = strings["load"]["noentry"]
            except discord.ExtensionAlreadyLoaded:
                string:str = strings["load"]["loaded"]
            except discord.ExtensionFailed as error:
                string:str = strings["load"]["failure"] + str(error) + "\n"
            print(string.format(name = i))
            continuous_string += string + "\n"
        return continuous_string

def cog_unloader(name:str|None = None) -> str:
    """If provided with name - unloads specific module.
    othervice unloads all default
    """
    if name:
        try:
            bot.unload_extension(name)
            string:str = strings["unload"]["success"]
        except discord.ExtensionNotFound:
            string:str = strings["load"]["notfound"]
        except discord.ExtensionNotLoaded:
            string:str = strings["load"]["notloaded"]
        print(string.format(name = name))
        return string
    else:
        continuous_string:str = ""
        for i in config["modules"]:
            try:
                bot.unload_extension(i)
                string:str = strings["unload"]["success"]
            except discord.ExtensionNotFound:
                string:str = strings["load"]["notfound"]
            except discord.ExtensionNotLoaded:
                string:str = strings["load"]["notloaded"]
            print(string.format(name = i))
            continuous_string += string + "\n"
        return continuous_string

@bot.command(name="load", hidden=True, aliases=["l"])
async def load(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    if ctx.author.id in config["administrators"]:
        return await ctx.reply(cog_loader(name))

@bot.command(name="unload", hidden=True, aliases=["u"])
async def unload(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    if ctx.author.id in config["administrators"]:
        return await ctx.reply(cog_unloader(name))

@bot.command(name="reload", hidden=True, aliases=["r"])
async def reload(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    author:discord.Member = ctx.author
    if author.id in config["administrators"]:
        return await ctx.reply(cog_unloader(name) + "\n" + cog_loader(name))

@bot.command(name="update", hidden=True)
async def update(ctx:commands.Context, action:str|None) -> discord.Message|None:
    """Function to check for update, apply update, or update if there is new version. Usage:\n
    No argument - Force updates, only for MEEE\n
    "check" - checks repo, and reports if there is update\n
    """
    if action == "check":
        if check():
            return await ctx.reply("I am up to date!")
        else:
            return await ctx.reply("Okay, I need to be updated - contact owner pwease!")
    else:
        if ctx.author.id != 579704749277052938:
            return await ctx.reply("This function is to be used only by owner!")
        Popen(["python", "updater.py"])
        print("Bot is disconnecting!")
        await bot.close()
        print("Bot is disconnected!")

@bot.event
async def on_ready():
    """Loading modules on start"""
    cog_loader()
    print("Bot is connected!")

bot.run(token)
