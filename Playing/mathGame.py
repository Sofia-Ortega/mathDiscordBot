"""Testing if can use @client.event within function. You can't (i think)"""

import discord
from discord.ext import commands

client = discord.Client()

def sendEquation():
    @client.event
    async def on_message(msg):
        general_channel = client.get_channel(758164860252061729)
        await general_channel.send('1 + 1 =')