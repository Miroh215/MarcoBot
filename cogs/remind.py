import discord, asyncio
from discord.ext import commands


class Remind(commands.Cog):
    """
    1) Store user, message and time in dictionary
        a) key = username, values = (time to send, message) 
    2) Encrypt dictionary
    3) Store encryption key in .env
    4) Pickle dictionary into storage file
    5) Load pickle file on bot start up. 
    6) Remove dictionary entry after message sent. 
    """
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["remindme"])
    async def remind(self, ctx, time, unit, *, message):
        time = int(time)
        origTime = time
        start = str(unit)[0]
        if start == 's': 
            pass
        elif start == 'm': 
            time = time * 60
        elif start == 'h': 
            time = time * 60 * 60
        elif start == 'd': 
            time = (time * 60 * 60) * 24 
        else:
            print("Invalid unit of time.")
            await ctx.send("Invalid unit of time.")
        print(f"Reminding {ctx.message.author} in {origTime} {unit} about '{message}'")
        await ctx.send(f"Okay, I'll remind you in {origTime} {unit} about '{message}'.")
        await asyncio.sleep(time);
        await ctx.send(message)
        print(f"Reminded {ctx.message.author} about '{message}'.")


def setup(client):
    client.add_cog(Remind(client))
