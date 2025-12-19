"""V1T4 Cog for interfacing with backend-hosted LLM"""
# pylint: disable=line-too-long
import json
from time import time
from urllib3 import BaseHTTPResponse, request
import discord
from discord.ext import commands

DEBUG = True

class Chat():
    """Class that represents chat between user and bot"""
    def __init__(self, user_id:int, system_prompt:str, debug_log_entry:str) -> None:
        self.user_id:int = user_id
        self.default_prompt:str = system_prompt
        self.system_prompt:str = system_prompt
        self.dialogs:list[dict[str,str|int]] = [{"role":"system",
                                                 "content":self.system_prompt}]
        self.debug_log_entry:str = debug_log_entry

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

        response:str = r.json()["choices"][0]["message"]["content"]
        self.dialogs.append({"role":"assistant",
                             "content":response})

        if DEBUG:
            # replacement_table:dict[str, str] = {
            #     "{time}": str(int(time())),
            #     "{user_id}": str(self.user_id),
            #     "{is_clear}": str(False),
            #     "{user_prompt}": user_prompt,
            #     "{system_prompt}": self.system_prompt,
            #     "{generated}": response
            # }
            # temp_entry:str = self.debug_log_entry
            # for old, new in replacement_table.items():
            #     temp_entry = temp_entry.replace(old, new)
            # with open("AI_DEBUG_LOG.log", "at", encoding="UTF-8") as file:
            #     file.write(temp_entry)
            # del temp_entry, replacement_table
            entry:str = json.dumps({
                    "time": int(time()),
                    "user_id": self.user_id,
                    "is_clear": False,
                    "user_prompt": user_prompt,
                    "system_prompt": self.system_prompt,
                    "generated": response
                }, ensure_ascii=False)\
                    .replace("\"user_prompt\"", "\n  \"user_prompt\"")\
                    .replace("\"system_prompt\"", "\n  \"system_prompt\"")\
                    .replace("\"generated\"", "\n  \"generated\"") + "\n"
            with open("AI_DEBUG_LOG.log", "at", encoding="UTF-8") as file:
                file.write(entry)
        return response

    def reset(self) -> None:
        """Resets chat history."""
        self.dialogs = [{"role":"system",
                         "content":self.system_prompt}]

    def set_system_prompt(self, prompt:str) -> None:
        """Sets system prompt to user defined, or default if none provided."""
        self.system_prompt = self.default_prompt if prompt == "default" else prompt
        self.reset()

class Ai(commands.Cog):
    """
    This cog is designed to do AI interfacing, idk
    """

    def __init__(self, bot:commands.Bot) -> None:
        with open("Data/ai.json", "rt", encoding = "UTF-8") as file:
            data:dict = json.load(file)
            self.address:str = data["address"]
            self.model_endpoint:str = data["model_endpoint"]
            self.inference_endpoint:str = data["inference_endpoint"]
            self.default_prompt:str = data["default_prompt"]
            self.debug_log_entry:str = data["debug_log_entry"]
        del data
        r:BaseHTTPResponse = request(
            method = "GET",
            url = self.address + self.model_endpoint
        )
        self.model:str = r.json()["data"][0]["id"]
        del r
        self.chats:dict[int, Chat] = {}
        self.bot:commands.Bot = bot
        if self.bot.user is not None:
            self.bot_id:int = self.bot.user.id

    def cog_unload(self) -> None:
        print("goodbye world!")

    @commands.command(name = "clear")
    async def history_reset(self, ctx:commands.Context) -> discord.Message|None:
        """Wrapper to reset chat history"""
        # validating input
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        # just in case not initialized
        if ctx.author.id not in self.chats:
            self.chats[ctx.author.id] = Chat(ctx.author.id,
                                             self.default_prompt,
                                             self.debug_log_entry)
        # work itself
        self.chats[ctx.author.id].reset()
        return await ctx.reply("Chat history had been reset, nya!")

    @commands.command(name = "set_prompt")
    async def edit_system_prompt(self,
                                 ctx:commands.Context,
                                 *, system_prompt:str) -> discord.Message|None:
        """Resets history with bot"""
        # validating input
        if not isinstance(ctx.channel, discord.DMChannel):
            return
        # just in case not initialized
        if ctx.author.id not in self.chats:
            self.chats[ctx.author.id] = Chat(ctx.author.id,
                                             self.default_prompt,
                                             self.debug_log_entry)
        # work itself
        self.chats[ctx.author.id].set_system_prompt(system_prompt)
        return await ctx.reply("System prompt had been changed, nya!")

    @commands.Cog.listener("on_message")
    async def answer(self, message:discord.Message) -> discord.Message|None:
        """Gets user message and then generates an answer
        also logs userID, name, request, and generated answer - just in case"""
        if not isinstance(message.channel, discord.DMChannel)\
        or message.author.id == self.bot_id\
        or message.content.startswith("Meow, "):
            return
        if message.author.id not in self.chats:
            self.chats[message.author.id] = Chat(message.author.id,
                                                 self.default_prompt,
                                                 self.debug_log_entry)
        async with message.channel.typing():
            reply:str = self.chats[message.author.id].generate(
                self.address + self.inference_endpoint,
                self.model,
                message.content
            )
            # Checking if output is longer than discord message limit
            # And if it is - breaking it up into chunks
            if len(reply) > 2000:
                temp_str:str
                index:int
                out_str:str
                # Just for sake of right move - limiting amount of iterations
                for _ in reply:
                    if len(reply) < 2000:
                        break
                    temp_str = reply[:2000]
                    index = temp_str.rfind("\n")
                    # If there is no newlines!
                    if index < 0:
                        index = temp_str.rfind(" ")
                    #If there is not even spaces!
                    if index < 0:
                        index = 2000
                    # Breaking strings on found edge, hope this is okay to do it this way
                    out_str = reply[:index]
                    reply = reply[index:]
                    await message.channel.send(out_str)
        return await message.channel.send(reply)

def setup(bot:commands.Bot) -> None:
    """boilerplate"""
    bot.add_cog(Ai(bot))
