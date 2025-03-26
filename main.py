import sys
import json
from typing import Optional

import discord
from discord.ext import commands

try:
    with open("Data/token") as file:
        token = file.read()
except FileNotFoundError:
    token = ""

if token == "":
    if sys.stdin.isatty():
        token = input("File with token is empty, please enter valid token! (path: Data/token)\n > ")
        with open("Data/token", "wt") as file:
            file.write(token)
    else:
        print("No file and no terminal detected - create ./Data/token file with actual bot token!")
        exit(1)




with open("Data/config.json", "rt") as file:
    config = json.load(file)

with open("main_strings.json", "rt") as file:
    strings = json.load(file)

bot:commands.Bot = commands.Bot(command_prefix=config["prefix"], intents = discord.Intents.all())

def cog_loader(name:Optional[str] = None) -> str:
    if name:
        try:
            bot.load_extension("Modules."+name)
            string = strings["load"]["success"].format(name = name)
        except BaseException as error:
            string = strings["load"]["failure"].format(name = name, error = error)
        print(string)
        return string
    continuous_string = ""
    for i in config["modules"]:
        try:
            bot.load_extension("Modules."+i)
            string = strings["load"]["success"].format(name = name)
        except BaseException as error:
            string = strings["load"]["failure"].format(name = name, error = error)
        print(string)
        continuous_string += string + "\n"
    return continuous_string

def cog_unloader(name:Optional[str] = None) -> str:
    if name:
        try:
            bot.unload_extension(name)
            string = strings["unload"]["success"].format(name = name)
        except BaseException as error:
            string = strings["unload"]["failure"].format(name = name, error = error)
        print(string)
        return string
    continuous_string = ""
    for i in config["modules"]:
        try:
            bot.unload_extension(i)
            string = strings["unload"]["success"].format(name = name)
        except BaseException as error:
            string = strings["unload"]["failure"].format(name = name, error = error)
        print(string)
        continuous_string += string + "\n"
    return continuous_string

@bot.command(name="load", hidden=True, aliases=["l"])
async def load(ctx:commands.Context, name:Optional[str] = None) -> None:
    if ctx.author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_loader(name))

@bot.command(name="unload", hidden=True, aliases=["u"])
async def unload(ctx:commands.Context, name:Optional[str] = None) -> None:
    if ctx.author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_unloader(name))

@bot.command(name="reload", hidden=True, aliases=["r"])
async def reload(ctx:commands.Context, name:Optional[str] = None) -> None:
    if ctx.author.id in config["administrators"]: # type: ignore
        return await ctx.reply(cog_loader(name) + "\n" + cog_unloader(name))
    
bot.run(token)