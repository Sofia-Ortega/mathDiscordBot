"""

Followed Youtube Tutorial Series
    -Discord.py Rewrite Tutorial
    -Tech with Tim

"""

import discord
from generator import sumGenerator
token = 'NzcyOTk5MTgxNjI2NTA3MjY0.X6C1lg.00b2zKc3-9KnD6T6-Hn9C8W9H9Q'


client = discord.Client()
general_id = 758164860252061729

@client.event
async def on_ready():
    general_channel = client.get_channel(general_id)
    await general_channel.send('Ready to RUMBLE!')

@client.event
async def on_message(msg):
    user = msg.content
    if user == "Sofia is Awesome":
        print("It's true")
    elif user == "Manchas is Awesome":
        print("Even truer")
    elif user == "41":
        print("Something or other")

@client.event
async def on_disconnect():
    general_channel = client.get_channel(general_id)
    await general_channel.send("Goodbye")

client.run(token)