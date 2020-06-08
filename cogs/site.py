import discord, asyncio, os
from discord.ext import commands

class Site(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command()
    async def get_site_name(self, ctx):
        url = os.popen("curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"https:..([^\"]*).*/\1/p'").read()
        await ctx.send(url)


def setup(client):
    client.add_cog(Site(client))
