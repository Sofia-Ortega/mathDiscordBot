"""Practicing waiting for user to respond"""


import discord
from random import randint

token = 'NzcyOTk5MTgxNjI2NTA3MjY0.X6C1lg.00b2zKc3-9KnD6T6-Hn9C8W9H9Q'
general_id = 758164860252061729
client = discord.Client()



@client.event
async def on_message(message):
    if message.content.startswith('--start'):
        msg = ""
        channel = message.channel

        # quit if user types --quit
        while msg != '--quit':

            num1 = randint(1, 10)
            num2 = randint(1, 10)
            sum = num1 + num2
            equation = str(num1) + " + " + str(num2) + " = "
            await channel.send(equation)

            def check(m):
                # checks correct ans
                return m.content == str(sum) or m.content == '--quit'
            msg = await client.wait_for('message', check=check)

            # stops if user types --quit
            if msg.content == '--quit':
                break

            await channel.send('Correct!')




@client.event
async def on_ready():
    general_channel = client.get_channel(general_id)
    await general_channel.send("Lets gooooo")

client.run(token)