"""Main executor for code"""

import discord
from discord.utils import get,find
from discord.ext.commands import Bot
import time

import asyncio

from math_game.generator import eq_gen
import math_game.score as score
import config

token = config.CONFIG['token']
main_id = -1
bot_prefix = config.CONFIG['bot_prefix']
category_name = config.CONFIG['category']

agree = ['yes', 'y', 'ya', 'yah', 'yep', 'true']
disagree = ['no', 'n', 'na', 'nah', 'nay', 'false']

messages_to_new_members = False
try:
    intents=intents=discord.Intents.all()
    client = Bot(command_prefix=bot_prefix,intents=intents)
    messages_to_new_members = True
except:
    client = Bot(command_prefix=bot_prefix)

client.remove_command('help')

# ---------------- GAMES ---------------- #
@client.command(name='start_math_game')
async def startMath(context, channel):
    c = channel
    await channel.send(':white_small_square::small_blue_diamond:Math Game:small_blue_diamond::white_small_square:')
    await channel.send(f'Type **{bot_prefix}stop** if you want to stop playing')

    def check_lvl(reaction, user):
        return user == context.author

    difficulty_question = await channel.send("Would you like 'easy', 'medium', or 'hard' level?")
    await difficulty_question.add_reaction('🟩')
    await difficulty_question.add_reaction('🟨')
    await difficulty_question.add_reaction('🟥')
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check_lvl)
    except asyncio.TimeoutError:
            difficulty = 'easy'

    if str(reaction.emoji) == '🟩':
        difficulty = 'easy'
    elif str(reaction.emoji) == '🟨':
        difficulty = 'medium'
    else:
        difficulty = 'hard'
    
    timed_question = await channel.send('Timed or not timed?')
    await timed_question.add_reaction('👍')
    await timed_question.add_reaction('👎')

    def check_react(reaction, user):
            return user == context.author

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check_react)
    except asyncio.TimeoutError:
        time_mode = False
    else:
        if str(reaction.emoji) == '👍':
            time_mode = True
        else:
            time_mode = False

    def check_int(m):
        return (m.content.isdigit() or m.content == f'{bot_prefix}stop') and m.channel.id == channel.id

    if time_mode:
        questNum = 100
        def check_sec(m):
            return (m.content.isdigit() or m.content == f'{bot_prefix}stop') and channel.id == m.channel.id


        await channel.send("Enter the game length in seconds: ")
        msg = await client.wait_for('message', check=check_int)
        time_desired = int(msg.content)

    else:
        await channel.send("Please enter the number of math question you would like: ")
        msg = await client.wait_for('message', check=check_int)
        questNum = int(msg.content)

    def timer(end):
        """returns false if time runs out and in time_mode"""
        if time_mode:
            return not(time.time() > end)
        else:
            return True

    def continue_game(m,end):
        if m.content == f'{bot_prefix}stop':
            return False
        elif not(timer(end)):
            return False
        elif not time_mode and questNum <= 0:
            return False
        return True
    
    # Starting Game
    countdown = 4
    while (countdown > 0):
        if (countdown == 4):
            await channel.send('Ready?')
        elif (countdown == 3):
            await channel.send(':red_circle:  ' + str(countdown))
        elif (countdown == 2):
            await channel.send(':yellow_circle:  ' + str(countdown))
        elif (countdown == 1):
            await channel.send(':green_circle:  ' + str(countdown))
        time.sleep(1)
        countdown = countdown - 1
    
    endTime = 0
    if time_mode:
        startTime = time.time()
        endTime = startTime + time_desired

    # stop if user types {bot_prefix}stop
    while continue_game(msg, endTime):
        
        equation, answer = eq_gen(difficulty)
        await channel.send(':small_blue_diamond: ' + equation)
        

        def checkAns(m):
             # checks correct answer to equation
            return (m.content == str(answer) or m.content == f'{bot_prefix}stop') and m.channel.id == channel.id

        msg = await client.wait_for('message', check=checkAns)

        if msg.content != f'{bot_prefix}stop':
            score.update_score(channel.id, msg.author.name)
            questNum -= 1
        
        if msg.content == f'{bot_prefix}stop':
            return

    # if stop is never called
    await channel.send('Game over!')
    await channel.send(score.get_final_score(channel.id))
    score.reset_score(channel.id)

    time.sleep(1)
    await context.invoke(client.get_command('play_again'), channel)


# ---------------- COMMANDS ---------------- #
@client.command(name='start')
async def startGame(context):
    channel_id = await context.invoke(client.get_command('new_channel'))
    channel = client.get_channel(channel_id)
    await channel.send('Hey there, <@' + str(context.message.author.id) + '>')
    
    embedVar = discord.Embed(title='Game Time!', description='', color=0x800000)
    embedVar.add_field(name='To add players: ', value=f'{bot_prefix}add @player', inline=True)
    embedVar.add_field(name='When you are ready to play: ', value=f'{bot_prefix}play', inline=False)
    await channel.send(embed=embedVar)

    def checkMsg(m):
        # checks correct ans
        return m.content == f'{bot_prefix}play' and m.channel.id == channel_id

    play = False
    while not play:
        play = await client.wait_for('message', check=checkMsg)
    
    await client.loop.create_task(gamePrompt(context,channel))
    #await context.invoke(client.get_command('game_prompt'), channel)




@client.command(name='quit')
async def quitGame(context, channel):
    prompt = await channel.send('Would you like to play another game?')

    def check_lvl(reaction, user):
        return user == context.author

    await prompt.add_reaction('✅')
    await prompt.add_reaction('❌')
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check_lvl)
    except asyncio.TimeoutError:
        again = False

    if str(reaction.emoji) == '✅':
        again = True
    elif str(reaction.emoji) == '❌':
        again = False
    
    if again:
        await context.invoke(client.get_command('game_prompt'), channel)
    else:
        await channel.delete()


@client.command(name='stop')
async def stopGame(context):
    channel = client.get_channel(context.channel.id)
    await channel.send('Game over!')
    if bool(score.score[channel.id]):
        await channel.send(score.get_final_score(channel.id))
        score.reset_score(channel.id)

    await context.invoke(client.get_command('play_again'), channel)


@client.command(name='play_again')
async def playAgain(context, channel):
    prompt = await channel.send('Would you like to play another game?')

    def check_lvl(reaction, user):
        return user == context.author

    await prompt.add_reaction('✅')
    await prompt.add_reaction('❌')
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check_lvl)
    except asyncio.TimeoutError:
        again = False

    if str(reaction.emoji) == '✅':
        again = True
    elif str(reaction.emoji) == '❌':
        again = False
    
    if again:
        await context.invoke(client.get_command('game_prompt'), channel)
    else:
        await channel.delete()


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
async def gamePrompt(context, c):
    prompt = await c.send('\nWhat game would you like to play?\nMath Game: 💡')
    await prompt.add_reaction('💡')

    def check_react(reaction, user):
            return (user == context.author and reaction.message.channel.id == c.id and str(reaction.emoji) == '💡')

    math = False
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=360.0, check=check_react)
    except asyncio.TimeoutError:
        math = False
    else:
        if str(reaction.emoji) == '💡':
            math = True
        # else if for other games ... or create a dictionary for this selection
        else:
            math = False
    
    if math:
        await startMath(context, c)


@client.command(name='play')
async def playGame(context):
    return

def makeInfoEmbed():
    embed=discord.Embed(title="**Game Bot**", description="A bot made for playing games and having fun! Invite your friends along or try to beat your scores! We could all use a little fun, what better way than to play some games right here on discord.\n-----------------------------", color=0x800000)
    embed.add_field(name=f"`{bot_prefix}help`", value="List of commands", inline=False)
    embed.add_field(name=f"`{bot_prefix}start`", value="Initiate a game session\n-----------------------------", inline=False)
    embed.add_field(name='Once you start a game:', value="-----------------------------", inline=False)
    embed.add_field(name=f"`{bot_prefix}add @player`", value="Add player to your session", inline=False)
    embed.add_field(name=f"`{bot_prefix}play`", value="Ready to play! Choose your game mode.", inline=False)
    embed.add_field(name=f"`{bot_prefix}stop`", value="End the game", inline=False)
    embed.add_field(name="Source Code", value="https://github.com/Sofia-Ortega/mathDiscordBot", inline=False)
    embed.set_footer(text="Created by Sofia Ortega and Andrew Fennell")
    return embed

@client.command(name='info')
async def info(context):
    channel_id = context.channel.id
    channel = client.get_channel(channel_id)
    embed = makeInfoEmbed()
    await channel.send(embed=embed)

@client.command(name='help')
async def help(context):
    await context.invoke(client.get_command('info'))


# ---------------- EVENTS ---------------- #
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(embed=makeInfoEmbed())
        main_id = general

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(main_id)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games..."))
    await general_channel.send("Beep Boop. Powering on...")
    await general_channel.send(embed=makeInfoEmbed())

@client.event
async def on_member_join(member):
    if messages_to_new_members:
        await member.send(embed=makeInfoEmbed())


# ---------------- INIT ---------------- #
client.run(token)
