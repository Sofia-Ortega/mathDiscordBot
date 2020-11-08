"""Main executor for code"""

import discord
from discord.utils import get
from discord.ext.commands import Bot
import time
import asyncio
from generator import eq_gen

import score
import config

token = config.CONFIG['token']
main_id = config.CONFIG['channel_id']
bot_prefix = config.CONFIG['bot_prefix']
category_name = config.CONFIG['category']

agree = ['yes', 'y', 'ya', 'yah', 'yep']
disagree = ['no', 'n', 'na', 'nah', 'nay']

client = Bot(command_prefix=bot_prefix)

# ---------------- GAMES ---------------- #
@client.command(name='start_math_game')
async def startMath(context, channel):

    await channel.send(':white_small_square::small_blue_diamond::white_small_square::small_blue_diamond::white_small_square:')
    await channel.send(f'Type {bot_prefix}quit if you want to stop playing')
    timed_question = await channel.send('Would you like to be timed?')
    await timed_question.add_reaction('👍')
    await timed_question.add_reaction('👎')

    def check_react(reaction, user):
            return user == context.author

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_react)
    except asyncio.TimeoutError:
        time_mode = False
    else:
        if str(reaction.emoji) == '👍':
            time_mode = True
        else:
            time_mode = False

    def check_int(m):
        return m.content.isdigit() or m.content == f'{bot_prefix}quit'

    if time_mode:
        questNum = 100
        def check_sec(m):
            return m.content.isdigit() or m.content == f'{bot_prefix}quit'


        await channel.send("How many seconds would you like (Enter an integer): ")
        msg = await client.wait_for('message', check=check_int)
        time_desired = int(msg.content)

        startTime = time.time()
        endTime = startTime + time_desired

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
        elif not time_mode and questNum <= 0:
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


# ---------------- COMMANDS ---------------- #
@client.command(name='start')
async def startGame(context):
    channel_id = await context.invoke(client.get_command('new_channel'))
    channel = client.get_channel(channel_id)
    await channel.send('Hey there, <@' + str(context.message.author.id) + '>')
    
    embedVar = discord.Embed(title='Game Time!', description='', color=0xFFFFFF)
    embedVar.add_field(name='Adding players: ', value=f'{bot_prefix}add <tag player>', inline=True)
    embedVar.add_field(name='Ready to choose game: ', value=f'{bot_prefix}done', inline=False)
    await channel.send(embed=embedVar)

    def checkMsg(m):
        # checks correct ans
        return m.content == f'{bot_prefix}done'

    done = False
    while not done:
        done = await client.wait_for('message', check=checkMsg)
    
    await context.invoke(client.get_command('game_prompt'), channel)


@client.command(name='quit')
async def stopGame(context):
    channel = client.get_channel(context.channel.id)
    if not bool(score.score):
        return
    await channel.send(score.get_final_score())
    score.reset_score()


@client.command(name='new_channel')
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


@client.command(name='add')
async def addUserToSession(context, member):
    channel_id = context.channel.id
    channel = client.get_channel(channel_id)
    try:
        member_id = member.split('@')[1].split('>')[0]
    except:
        await channel.send('User not found.')
        return
    try:
        user = client.get_user(int(member_id)) # discord.User type
    except:
        await channel.send('User not found.')
        return
    if user: # if user is found
        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.send(f'{user.name} has been added.')
    else: # if user is not found
        await channel.send('User not found.')


@client.command(name='game_prompt')
async def gamePrompt(context, channel):
    prompt = await channel.send('\nWhat game would you like to play?\nMath Game: 💡')
    await prompt.add_reaction('💡')

    def check_react(reaction, user):
            return user == context.author

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_react)
    except asyncio.TimeoutError:
        math = False
    else:
        if str(reaction.emoji) == '💡':
            math = True
        # else if for other games ... or create a dictionary for this selection
        else:
            math = False
    
    if math:
        await context.invoke(client.get_command('start_math_game'), channel)

@client.command(name='done')
async def doneTask(context):
    return


# ---------------- EVENTS ---------------- #
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(main_id)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games..."))
    await general_channel.send("How do you do?")


# ---------------- INIT ---------------- #
client.run(token)
