# Game Bot

A bot made for playing games and having fun!
The bot is made for Discord using discord.py.

## Setup

1. Configure your desired settings in config.py
`token` - Token for your bot
`channel_id` - Channel that the bot will send certain commands, though the bot will work throughout the server
`category` - Optional, if you want game channels to be created in a particular category in the server
`bot_prefix` - This will be the prefix character(s) needed to activate commands (i.e. !start or -start)

## Running The Bot

## Commands
The beginning character will be based on how `bot_prefix` is configured in config.py
`!start` - Initiate a game session
`!add @player` - Add player to your session
`!play` - Ready to play! Choose your game.
`!stop` - End the game, or play a different one
