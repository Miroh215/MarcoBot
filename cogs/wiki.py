import discord, wikipedia
from discord.ext import commands


class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['w', 'wikipedia'])
    async def wiki(self, ctx, *, terms):
        terms = terms.split(',')
        for term in terms:
            try:
                await ctx.send(wikipedia.summary(term, sentences=2))
            except wikipedia.DisambiguationError as e:
                await ctx.send(e)


def setup(client):
    client.add_cog(Wiki(client))
