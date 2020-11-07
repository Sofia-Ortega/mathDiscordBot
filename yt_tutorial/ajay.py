"""

Followed Youtube Tutorial Series
    -(2020) How to Code Your Own Discord Bot in Python
    -Ajay Gandecha

"""

# import module
import discord
from discord.ext import commands

# Client (our bot)
# client = discord.Client()
client = commands.Bot(command_prefix="--")

@client.command(name='start')
async def start(msg):

    myEmbed = discord.Embed(title="Jokes", description="Imagine something really funny is right here", color=0x4287f)
    myEmbed.add_field(name="Cheesy joke", value="Want to hear a cheesy joke...nevermind, its too CHEESY", inline=False)
    myEmbed.add_field(name="Unexpected Joke",
                      value="I used to wonder why fribees looked bigger the closer they got...And then it hit me")
    myEmbed.set_footer(text="The best footer")
    myEmbed.set_author(name="Sofia and Mr. Spears")

    await msg.message.channel.send(embed=myEmbed)


@client.event
async def on_ready():
    # DO STUFF...
    general_channel = client.get_channel(758164860252061729)
    await general_channel.send('Hello Discord!!!')

@client.event
async def on_message(msg):
    if msg.content == '!start':
        general_channel = client.get_channel(758164860252061729)

        myEmbed = discord.Embed(title="Jokes", description="Imagine something really funny is right here", color=0x4287f)
        myEmbed.add_field(name="Cheesy joke", value="Want to hear a cheesy joke...nevermind, its too CHEESY", inline=False)
        myEmbed.add_field(name="Unexpected Joke", value="I used to wonder why fribees looked bigger the closer they got...And then it hit me")
        myEmbed.set_footer(text="The best footer")
        myEmbed.set_author(name="Sofia and Mr. Spears")

        await general_channel.send(embed=myEmbed)
    await client.process_commands(msg)

@client.event
async def on_disconnect():
    general_channel = client.get_channel(758164860252061729)
    await general_channel.send('Forgive me, my alien parents call me')

# Run the client on the server
# will be regenerated after posted on github
client.run('NzcyOTk5MTgxNjI2NTA3MjY0.X6C1lg.00b2zKc3-9KnD6T6-Hn9C8W9H9Q')

