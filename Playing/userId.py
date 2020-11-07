"""Practice getting userId"""


import discord

client = discord.Client()
token = 'NzcyOTk5MTgxNjI2NTA3MjY0.X6C1lg.00b2zKc3-9KnD6T6-Hn9C8W9H9Q'
general_id = 758164860252061729

@client.event
async def on_ready():
    general_channel = client.get_channel(general_id)
    await general_channel.send("RAAAWWWRRR\nDo newlines work?")


@client.event
async def on_message(message):
    print(message.author)

client.run(token)