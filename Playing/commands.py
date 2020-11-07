"""Expermenting with commands"""

import discord
from discord.ext import commands


general_id = 758164860252061729
token = 'NzcyOTk5MTgxNjI2NTA3MjY0.X6C1lg.00b2zKc3-9KnD6T6-Hn9C8W9H9Q'

client = commands.Bot(command_prefix="--")

@client.command(name="start")
async def start(msg):
    print(msg)

    general_channel = client.get_channel(general_id)
    await general_channel.send("Hold your horses")


@client.event
async def on_ready():
    general_channel = client.get_channel(general_id)
    await general_channel.send("Client events still work")


client.run(token)