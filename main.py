import time as t
import requests
import os
import discord
import json
import textwrap
import traceback
import io
import sys
import datetime
from contextlib import redirect_stdout
import re
from get_song import get_current_song

# Import other functions / files / needed packages
from discord.ext import commands
from dotenv import load_dotenv


# Load the token from the .env file
load_dotenv()

# Get the token from the .env file
token = os.getenv("token")

# Set the configuration from the config.json file
with open("config/config.json", "r") as f:
    config = json.load(f)
    prefix = config.get("prefix")
    main_account_id = config.get("main_account_id")

print("This is a discord selfbot, this is to be run on a bot account. This is not automating user accounts, as that is against discord's ToS.")


# Set the intents
intents = discord.Intents.default()  # Sets the default bot intents
intents.guilds = True
intents.members = True  # Allows the bot to see members in a guild
intents.message_content = True  # Allows the bot to see message content


# set bot
bot = commands.Bot(command_prefix=prefix, intent=intents)


# Def is owner check
def is_owner(ctx):
    return ctx.author.id == main_account_id



# Set Eval Command
@bot.command(hidden=True, name='eval')
@commands.check(is_owner)
async def eval(ctx, *, body: str):
    """Evaluates a code"""

    if "print(TOKEN)" in body:
        return await ctx.send("You wish")

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except discord.Forbidden:
        await ctx.send('I do not have permission to perform this action.')
    except discord.HTTPException as http_ex:
        await ctx.send(f'HTTPException: {http_ex}')
    except discord.InvalidArgument as inv_arg:
        await ctx.send(f'InvalidArgument: {inv_arg}')
    except IndexError as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}IndexError: list index out of range\n{traceback.format_exc()}\n```')
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')

# Cleaning up the code
def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')

@bot.command(hidden=True, name='afk')
@commands.check(is_owner)
async def set_afk(ctx):
    """Sets the bot as afk"""
    if not config.get("afk").get("enabled"):
        config["afk"]["enabled"] = True
        await ctx.send("AFK mode has been enabled.")
    else:
        config["afk"]["enabled"] = False
        await ctx.send("AFK mode has been disabled.")



@bot.command(hidden=True, name="send-song")
@commands.check(is_owner)
async def send_song(ctx):
    """Sends the current song to the channel"""
    if not config.get("spotify_token"):
        return await ctx.send("No Spotify token found.")
    
    # Get the current song from Spotify
    current_song = get_current_song(config.get("spotify_token"))
    
    await ctx.send(f"Currently playing: {current_song}")
    

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if config.get("afk").get("enabled"):
        if str(main_account_id) in message.content:
            await message.reply(config.get("afk").get("message"))
        

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@eval.error
async def eval_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        main_account = bot.get_user(main_account_id)
        await ctx.send(f"You do not have permission to run this command @{main_account}")



# Run the bot
bot.run(token)


