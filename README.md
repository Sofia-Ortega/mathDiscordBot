# Math Game Bot

A bot made for playing games and having fun! Invite your friends along or try to beat your scores!<br />
The bot is made for Discord using discord.py.<br />

## Hosting this bot yourself
The bot will be running on multiple servers on one instance.<br />
If you would like to host this bot yourself, following these instructions:<br />

1. Fork this github repository and clone into a private repository.<br />
2. Configure your desired settings in config.py<br />
    `token` - Token for your bot, found on the Discord Developer Portal<br />
    `category` - Optional, if you want game channels to be created in a particular category in the server<br />
    `bot_prefix` - This will be the prefix character(s) needed to activate commands (i.e. !start, -start, ?start)<br />
3. Deploy via https://dashboard.heroku.com

## Step by Step Guide

1. Type -start in any channel to create a game session<br />
2. The bot will create a private channel your game will be active.<br />
3. Feel free to add users with -add @player, make sure your TAG the player, rather than just type their name<br />
4. The bot will ask some questions throughout the game and setup. Reply with reaction buttons!<br />
5. Have fun! If at any point you want to stop, type -stop.<br />

We want this bot to be easy to use! If you have any issues or suggestions, open an issue and let us know!<br />

## Commands

`-start` - Initiate a game session<br />
`-add @player` - Add player to your session<br />
`-play` - Ready to play! Choose your game.<br />
`-stop` - End the game, or play a different one<br />


## Documentation

https://docs.google.com/document/d/1mFkZvgCi1YJQEzA1DRVQ-88jSvVf2Aci77bu760S1lw/edit?usp=sharing
