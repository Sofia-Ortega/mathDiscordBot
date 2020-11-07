"""Main executor for code"""

import discord
from generator import eq_gen
import score
import config

token = config.CONFIG['token']
general_id = config.CONFIG['channel_id']
client = discord.Client()


@client.event
async def on_message(message):
    # start game
    if message.content.startswith('--start'):
        score.reset_score()
        # setting up variables
        channel = message.channel

        def checkint(m):
            return m.content.isdigit() or m.content == '--quit'

        await channel.send("Please enter the number of math question you would like: ")
        msg = await client.wait_for('message', check=checkint)
        questNum = int(msg.content)

        # quit if user types --quit
        while msg.content != '--quit' and questNum > 0:


            equation, answer = eq_gen()
            await channel.send(equation)

            def checkAns(m):
                # checks correct ans
                return m.content == str(answer) or m.content == '--quit'

            msg = await client.wait_for('message', check=checkAns)

            if msg.content != "--quit":
                score.update_score(msg.author.name)
                questNum -= 1




        await channel.send(score.get_final_score())
        await channel.send('goodbye!')





@client.event
async def on_ready():
    general_channel = client.get_channel(general_id)
    await general_channel.send("Lets gooooo")

client.run(token)