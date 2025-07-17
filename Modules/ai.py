"""V1T4 Cog for interfacing with backend-hosted LLM"""

import json
from time import time
from urllib3 import request
import discord
from discord.ext import commands

DEBUG = True

class Chat():
    """Class that represents chat between user and bot"""
    def __init__(self, user_id:int, system_prompt:str) -> None:
        self.user_id:int = user_id
        self.default_prompt:str = system_prompt
        self.system_prompt:str = system_prompt
        self.dialogs:list[dict[str,str|int]] = [{"role":"system",
                                                 "content":self.system_prompt}]
    def generate(self, address:str, model:str, user_prompt:str) -> str:
        """Generates an output based on user prompt
        Returns string to print, also saves into instance"""
        self.dialogs.append({"role":"user",
                             "content":user_prompt})

        r = request(
            method = "POST",
            url = address,
            headers = {"Content-Type":"application/json"},
            json = {"model":model,"messages":self.dialogs},
            timeout = None
            )

        response = r.json()["choices"][0]["message"]["content"]
        self.dialogs.append({"role":"assistant",
                             "content":response})

        if DEBUG:
            with open("AI_DEBUG_LOG.log", "wt+", encoding="UTF-8") as file:
                file.write(json.dumps({"time":int(time()),
                                       "user_id":self.user_id,
                                       "user_prompt":user_prompt,
                                       "system_prompt":self.system_prompt,
                                       "generated":response})+"\n")

        return response

    def reset(self) -> None:
        """Resets chat history."""
        self.dialogs:list[dict[str,str|int]] = [{"time":int(time()),
                                                 "role":"system",
                                                 "content":self.system_prompt}]
        return

    def set_system_prompt(self, prompt:str|None=None) -> None:
        """Sets system propt to user defined, or default if none provided."""
        self.system_prompt = self.default_prompt if prompt is None else prompt
        return

class Ai(commands.Cog):
    """
    This cog is designed to do AI interfacing, idk
    """

    def __init__(self, bot:commands.Bot) -> None:
        # ToDo: migration towards SQLite, since json is not a DB
        # Kinda ironic from me, whom always said that "JSON is my DB"
        with open("Data/ai.json", "rt", encoding = "UTF-8") as file:
            data:dict = json.load(file)
            self.address = data["address"]
            self.model_endpoint = data["model_endpoint"]
            self.inference_endpoint = data["inference_endpoint"]
            self.default_prompt = data["default_prompt"]
        del data
        r = request(
            method = "GET",
            url = self.address + self.model_endpoint
        )
        self.chats:dict[int, Chat] = {}
        self.model = r.json()["data"]["id"]
        self.bot:commands.Bot = bot
        if self.bot.user is not None:
            self.bot_id = self.bot.user.id

    def cog_unload(self) -> None:
        print("goodbye world!")

    @commands.command(name = "History_reset")
    async def history_reset(self, ctx:commands.Context) -> discord.Message|None:
        """Wrapper to reset chat history"""
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        if ctx.author.id not in self.chats:
            self.chats[ctx.author.id] = Chat(ctx.author.id, self.default_prompt)
        self.chats[ctx.author.id].reset()
        return await ctx.reply("Chat history had been reset, nya!")

    @commands.command(name = "edit_system_message")
    async def edit_system_message(self, ctx:commands.Context, ) -> discord.Message|None:
        """Resets history with bot"""
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        if ctx.author.id not in self.chats:
            self.chats[ctx.author.id] = Chat(ctx.author.id, self.default_prompt)
        self.chats[ctx.author.id].set_system_prompt()
        return await ctx.reply("System prompt had been changed, nya!")

    @commands.Cog.listener("on_message")
    async def answer(self, message:discord.Message) -> discord.Message|None:
        """Gets user message and then generates an answer
        also logs userID, name, request, and generated answer - just in case"""
        if message.author.id == self.bot_id:
            return
        if not isinstance(message.channel, discord.DMChannel):
            return
        if message.author.id not in self.chats:
            self.chats[message.author.id] = Chat(message.author.id, self.default_prompt)
        reply = self.chats[message.author.id].generate(
            self.address + self.inference_endpoint,
            self.model,
            message.content
        )
        return await message.channel.send(reply)

def setup(bot:commands.Bot) -> None:
    """boilerplate"""
    bot.add_cog(Ai(bot))
