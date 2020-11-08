"""Main executor for code"""

import discord
from discord.utils import get
from discord.ext.commands import Bot
import time
from generator import eq_gen
import score
import config

token = config.CONFIG['token']
general_id = config.CONFIG['channel_id']
bot_prefix = config.CONFIG['bot_prefix']

agree = ['yes', 'y', 'ya', 'yah', 'yep']
disagree = ['no', 'n', 'na', 'nah', 'nay']

client = Bot(command_prefix=bot_prefix)

@client.command(name='start')
async def startMath(context):
    channel_id = await context.invoke(client.get_command('new_channel'))
    channel = client.get_channel(channel_id)
    await channel.send('Hey there, <@' + str(context.message.author.id) + '>')


    # check if user wants a timed mode
    def check_time(m):
        if m.content.lower() in agree or m.content.lower() in disagree:
            return True
        else:
            return False

    await channel.send('Would you like to be timed?')
    msg = await client.wait_for('message', check=check_time)

    time_mode = False
    if msg.content.lower() in agree:
        time_mode = True

    def check_int(m):
        return m.content.isdigit() or m.content == f'{bot_prefix}quit'

    if time_mode:
        questNum = 100
        def check_sec(m):
            return m.content.isdigit() or m.content == f'{bot_prefix}quit'

        await channel.send("How many seconds would you like (Enter an integer): ")
        msg = await client.wait_for('message', check=check_int)
        timer = int(msg.content)

        startTime = time.time()
        endTime = startTime + timer

    else:

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

    def timer():
        """returns false if time runs out and in time_mode"""
        if time_mode:
            return not(time.time() > endTime)
        else:
            return True

    def continue_game(m):
        if m.content == f'{bot_prefix}quit':
            return False
        elif not(timer()):
            return False
        elif not time_mode and questNum < 0:
            return False
        return True

    # quit if user types {bot_prefix}quit
    while continue_game(msg):

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
    await general_channel.send("How do you do?")

client.run(token)
