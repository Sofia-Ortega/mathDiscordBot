"""Main executor for code"""

import discord
from discord.utils import get
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
    channel_id = await context.invoke(client.get_command('new_channel'))
    channel = client.get_channel(channel_id)
    await channel.send('Hey there, <@' + str(context.message.author.id) + '>')

    def check_int(m):
            return m.content.isdigit() or m.content == f'{bot_prefix}quit'

    await channel.send("Please enter the number of math question you would like: ")
    msg = await client.wait_for('message', check=check_int)
    questNum = int(msg.content)

    def check_lvl(m):
        if m.content.lower() in {'easy', 'medium', 'hard'}:
            return True
        else:
            return False

    await channel.send("Would you like 'easy', 'medium', or 'hard' level?")
    msg = await client.wait_for('message', check=check_lvl)
    difficulty = msg.content

    # quit if user types {bot_prefix}quit
    while msg.content != f'{bot_prefix}quit' and questNum > 0:


        equation, answer = eq_gen(difficulty)
        await channel.send(equation)

        def checkAns(m):
            # checks correct ans
            return m.content == str(answer) or m.content == f'{bot_prefix}quit'

        msg = await client.wait_for('message', check=checkAns)

        if msg.content != f'{bot_prefix}quit':
            score.update_score(msg.author.name)
            questNum -= 1
        
        if msg.content == f'{bot_prefix}quit':
            return

    # if quit is never called
    await channel.send(score.get_final_score())
    score.reset_score()
    await channel.send('goodbye!')
        

@client.command(name='quit')
async def stopMath(context):
    channel = client.get_channel(general_id)
    if not bool(score.score):
        return
    await channel.send(score.get_final_score())
    score.reset_score()
    await channel.send('goodbye!')


@client.command(name='new_channel')
#@client.command(name='new_channel')
async def make_channel(context):
    guild = context.guild
    member = context.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
    }
    channel = await guild.create_text_channel('secret-channel', overwrites=overwrites)
    await channel.set_permissions(member, read_messages=True, send_messages=True)
    return channel.id


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(general_id)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games..."))
    await general_channel.send("Lets gooooo")

client.run(token)
