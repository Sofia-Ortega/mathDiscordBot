"""Main executor for code"""

import discord
from discord.utils import get
from discord.ext.commands import Bot
from generator import eq_gen
import score
import config

token = config.CONFIG['token']
main_id = config.CONFIG['channel_id']
bot_prefix = config.CONFIG['bot_prefix']
category_name = config.CONFIG['category']

client = Bot(command_prefix=bot_prefix)

@client.command(name='start')
async def startMath(context):
    channel_id = await context.invoke(client.get_command('new_channel'))
    channel = client.get_channel(channel_id)
    await channel.send('Hey there, <@' + str(context.message.author.id) + '>')

    def checkint(m):
            return m.content.isdigit() or m.content == f'{bot_prefix}quit'

    await channel.send(f'Type "{bot_prefix}quit" to stop playing...')
    await channel.send("Please enter the number of math question you would like: ")
    msg = await client.wait_for('message', check=checkint)
    questNum = int(msg.content)

    # quit if user types {bot_prefix}quit
    while msg.content != f'{bot_prefix}quit' and questNum > 0:


        equation, answer = eq_gen()
        await channel.send(':large_blue_diamond:\t' + equation + '\t:large_blue_diamond:')

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
        

@client.command(name='quit')
async def stopMath(context):
    channel = client.get_channel(context.channel.id)
    if not bool(score.score):
        return
    await channel.send(score.get_final_score())
    score.reset_score()


@client.command(name='new_channel')
#@client.command(name='new_channel')
async def make_channel(context):
    guild = context.guild
    member = context.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
    }

    if category_name == '': # if a category is not defined in config
        category = discord.utils.get(context.guild.categories)
    else: # if a category is defined in config
        category = discord.utils.get(context.guild.categories, name=category_name)

    channel = await guild.create_text_channel(f'{context.message.author.name}s-game', overwrites=overwrites, category=category)
    await channel.set_permissions(member, read_messages=True, send_messages=True)
    return channel.id


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(main_id)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games..."))
    await general_channel.send("Lets gooooo")

client.run(token)
