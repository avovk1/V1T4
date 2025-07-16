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
        self.system_prompt:str = system_prompt
        self.dialogs:list[dict[str,str|int]] = [{"time":int(time()),
                                                 "role":"system",
                                                 "content":self.system_prompt}]
    def generate(self, address:str, model:str, user_prompt:str) -> str:
        """Generates an output based on user prompt
        Returns string to print, also saves into instance"""
        self.dialogs.append({"time":int(time()),
                             "role":"user",
                             "content":user_prompt})
        r = request(
            method = "POST",
            url = address,
            headers = {"Content-Type":"application/json"},
            json = {"model":model,"messages":self.dialogs},
            timeout = None
            )
        response = r.json()["choices"][0]["message"]["content"]
        self.dialogs.append({"time":int(time()),
                             "role":"assistant",
                             "content":response})
        
        return ""
        

class Ai(commands.Cog):
    """
    This cog is designed to do AI interfacing, idk
    """

    def __init__(self, bot:commands.Bot) -> None:
        # ToDo: migration towards SQLite, since json is not a DB
        # Kinda ironic from me, whom always said that "JSON is my DB"
        with open("Data/ai.json", "rt", encoding = "UTF-8") as file:
            self.data:dict = json.load(file)
            self.address = self.data["address"]
            self.model_endpoint = self.data["model_endpoint"]
            self.inference_endpoint = self.data["inference_endpoint"]
            self.system_prompt = self.data["system_prompt"]
        r = request(
            method = "GET",
            url = self.address + self.model_endpoint
        )
        self.model = r.json()["data"]["id"]
        self.history = {}
        self.bot:commands.Bot = bot

    def cog_unload(self) -> None:
        print("goodbye world!")


    def get_history(self, user_id) -> list[dict[str, str]]:
        if user_id not in self.history:
            self.history[user_id] = []







        return [{"role":"system", "content":""}]


    @commands.command(name = "History_reset")
    async def history_reset(self, _ctx:commands.Context) -> discord.Message|None:
        """Resets history with bot"""
        return
    
    @commands.command(name = "edit_system_message")
    async def edit_system_message(self, _ctx:commands.Context) -> discord.Message|None:
        """Resets history with bot"""
        return

    @commands.Cog.listener("on_message")
    async def answer(self, _ctx:commands.Context) -> discord.Message|None:
        """Gets user message and then generates an answer
        also logs userID, name, request, and generated answer - just in case"""
        return

def setup(bot:commands.Bot) -> None:
    """boilerplate"""
    bot.add_cog(Ai(bot))
