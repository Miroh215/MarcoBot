import discord, random
from discord.ext import commands


class RPS(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.choices = ['rock', 'paper', 'scissors']
        self.results = { 'rock'     : { 'win' : 'scissors'},
                         'paper'    : { 'win': 'rock'},
                         'scissors' : {'win': 'paper'}
        }

    @commands.command()
    async def rps(self, ctx, throw):
        cpu = random.choice(self.choices)
        throw = throw.lower()
        if throw in self.choices:
            pass
        else:
            await ctx.send(f'{throw} is not a valid move. Try again.')
            return
        if cpu == throw.lower():
            await ctx.send(f"Wow you both threw {throw}. It's a tie!")
        elif self.results[throw]['win'] == cpu:
            await ctx.send(f"Your {throw} beats the computer's {cpu}. You win!")
        else:
            await ctx.send(f"I can't believe you threw {throw} when the computer threw {cpu}. You lose...")


def setup(client):
    client.add_cog(RPS(client))
