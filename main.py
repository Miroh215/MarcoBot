import discord, os, random, asyncio, praw
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

load_dotenv()
client = commands.Bot(command_prefix = '!')
activities = os.getenv("activities").split(',')
status = random.choice(activities)

@client.event
async def on_ready():
    await chooseActivity()
    await client.change_presence(activity=discord.Game(str(status)))
    # check.start()
    print('Bot is ready')

@client.command()
async def ping(ctx):
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.event
async def on_member_join(member):
    print(f'Welcome to the real world {member}!')

@client.event
async def on_member_remove(member):
    print(f'{member} has abondoned the real world.')

@client.event
async def chooseActivity():
    global status
    status = random.choice(activities)


@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'Without a doubt.',
                 'Ask again later.',
                 "Don't count on it.",
                 'Very Doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

@commands.is_owner()
@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        print(f"{extension} successfully loaded!")
        await ctx.send(f'{extension} successfully loaded!')
    except discord.ext.commands.ExtensionNotFound:
        print(f"{extension} not found.")
        await ctx.send(f"{extension} not found.")
    except discord.ext.commands.ExtensionAlreadyLoaded:
        print(f"{extension} already loaded.")
        await ctx.send(f"{extension} already loaded.")
    except discord.ext.commands.ExtensionFailed:
        print(f"{extension} has no valid setup function.")
        await ctx.send(f"{extension} has no valid setup function.")

@commands.is_owner()
@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        print(f"{extension} successfully unloaded.")
        await ctx.send(f'{extension} successfully unloaded.')
    except discord.ext.commands.ExtensionNotLoaded:
        print(f"{extension} already unloaded.")
        await ctx.send(f"{extension} already unloaded.")


@commands.is_owner()
@client.command()
async def reload(ctx, extension):
    try:
        client.reload_extension(f'cogs.{extension}')
        print(f"{extension} successfully reloaded!")
        await ctx.send(f'{extension} successfully reloaded!')
    except discord.ext.commands.ExtensionNotLoaded:
        print(f"{extension} not loaded.")
        await ctx.send(f"{extension} not loaded.")
    except discord.ext.commands.ExtensionNotFound:
        print(f"{extension} not found.")
        await ctx.send(f"{extension} not found.")
    except discord.ext.commands.NoEntryPointError:
        print(f"{extension} has no valid setup function.")
        await ctx.send(f"{extension} has no valid setup function.")
    except discord.ext.commands.ExtensionFailed:
        print(f"{extension}'s setup function has an execution error.")
        await ctx.send(f"{extension}'s setup function has an execution error.")

# @client.command(pass_context=True)
# async def dm(user: discord.User, * , message):
#     await client.send_message(user, message)        

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv("discordToken"))
