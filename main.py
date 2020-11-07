"""Main executor for code"""

import discord
from discord.ext.commands import Bot
from generator import eq_gen
import score
import config

token = config.CONFIG['token']
general_id = config.CONFIG['channel_id']
bot_prefix = config.CONFIG['bot_prefix']

client = Bot(command_prefix=bot_prefix)

@client.command(name='start')
async def startMath(context):
    channel = client.get_channel(general_id)

    def checkint(m):
            return m.content.isdigit() or m.content == f'{bot_prefix}quit'

    await channel.send("Please enter the number of math question you would like: ")
    msg = await client.wait_for('message', check=checkint)
    questNum = int(msg.content)

    # quit if user types {bot_prefix}quit
    while msg.content != f'{bot_prefix}quit' and questNum > 0:


        equation, answer = eq_gen()
        await channel.send(equation)

        def checkAns(m):
            # checks correct ans
            return m.content == str(answer) or m.content == f'{bot_prefix}quit'

        msg = await client.wait_for('message', check=checkAns)

        if msg.content != f'{bot_prefix}quit':
            score.update_score(msg.author.name)
            questNum -= 1
        

@client.command(name='quit')
async def stopMath(context):
    channel = client.get_channel(general_id)
    await channel.send(score.get_final_score())
    await channel.send('goodbye!')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(general_id)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games"))
    await general_channel.send("Lets gooooo")

client.run(token)
