import sys
import json
# import time
# from multiprocessing import Process


import discord
from discord.ext import commands
# import git

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
        token = ""
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
        try:
            bot.load_extension("Modules."+name)
            string:str = strings["load"]["success"]
        except discord.ExtensionNotFound:
            string:str = strings["load"]["notfound"]
        except discord.NoEntryPointError:
            string:str = strings["load"]["noentry"]
        except discord.ExtensionAlreadyLoaded:
            string:str = strings["load"]["loaded"]
        except discord.ExtensionFailed as error:
            string:str = strings["load"]["failure"] + error + "\n"
        string:str = string.format(name = name)
        print(string)
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
                string:str = strings["load"]["failure"] + error + "\n"
            string:str = string.format(name = name)
            print(string)
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
        string:str = string.format(name = name)
        print(string)
        return string
    else:
        continuous_string = ""
        for i in config["modules"]:
            try:
                bot.unload_extension(i)
                string:str = strings["unload"]["success"]
            except discord.ExtensionNotFound:
                string:str = strings["load"]["notfound"]
            except discord.ExtensionNotLoaded:
                string:str = strings["load"]["notloaded"]
            string:str = string.format(name = name)
            print(string)
            continuous_string += string + "\n"
        return continuous_string

@bot.command(name="load", hidden=True, aliases=["l"])
async def load(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    if ctx.author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_loader(name))

@bot.command(name="unload", hidden=True, aliases=["u"])
async def unload(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    if ctx.author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_unloader(name))

@bot.command(name="reload", hidden=True, aliases=["r"])
async def reload(ctx:commands.Context, name:str|None = None) -> discord.Message|None:
    """Discord interface function"""
    author:discord.Member = ctx.author
    if author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_unloader(name) + "\n" + cog_loader(name))

# @bot.command(name="update", hidden=True)
# async def update(ctx:commands.Context, action:str|None) -> discord.Message|None:
#     """Function to check for update, apply update, or update if there is new version. Usage:\n
#     "check" or no argument - checks repo, and reports if there is update\n
#     "update" - updates, if there is new version, dont use it willy-nilly\n
#     "update-soft" - updates only modules, without bot downtime\n
#     "schedule" - plans update to some point in time, where update will cause least amount of problems\n
#     "schedule-soft" - plans update of only modules\n
#     """
#     repo:git.Repo = git.Repo("./.git")
#     match action:
#         case "check"|None:
#             pass
#         case "update":
#             pass
#         case "update-soft":
#             pass
#         case "schedule":
#             pass
#         case "schedule-soft":
#             pass
#         case _:
#             pass

bot.run(token)
