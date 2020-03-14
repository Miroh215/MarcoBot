import discord, praw, os, asyncio, config
from discord.ext import commands

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)

class CheckReddit(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def meme(self, ctx, num=1):
        if isinstance(num,int):
            used = []
            for i in range(num):
                element = reddit.subreddit("memes").random()
                while element in used:
                    element = reddit.subreddit("memes").random()
                used.append(element)
                msg = discord.embeds.Embed(title=element.title, type="rich", url=element.url, description=f"score of: {element.score}", color=0xFF0000)
                msg.set_image(url=element.url)
                msg.set_author(name=element.author.name)
                await ctx.send(embed=msg)
                print("Meme delivered")
        else:
            await ctx.send("Please input a valid number.")

    @commands.command(aliases=['rc'])
    async def comments(self, ctx, sub, *, term):

        # term = term.lower()
        term = term.split(",")

        for item in term:
            # if item in config.preset_terms:
            try:
                [term.append(x) for x in config.preset_terms[item.lower()]]
            except:
                pass

        temp = []
        [temp.append(x.lower()) for x in term if x.lower() not in temp]

        term = temp

        subreddit = reddit.subreddit(sub)
        print("Searching...")
        await ctx.send("Searching...")
        results = 0
        sorting = subreddit.hot()
        found = False
        sep = '-'*50
        await ctx.send(term)
        for submission in sorting:
            # for word in submission.title:
            for comment in submission.comments:
                output = ''
                await asyncio.sleep(0)                
                out = False
                if isinstance(comment, praw.models.MoreComments):
                    continue
                for phrase in term:
                    try:
                        if len(comment.body) < 2000:
                            if phrase in comment.body.lower():
                                found = True
                                out = True
                                output += f'\n{sep}\n'
                                output += (f"""Post Title: {submission.title}
                                \nComment: {comment.body}
                                    \nhttps://www.reddit.com{comment.permalink}?context=10""")
                                output += f'\n{sep}\n'
                                results += 1
                                await ctx.send(output)
                                break
                            if out:
                                break
                    except:
                        pass
        if found:
            print(f"Search Completed, {results} results.")
            await ctx.send(f"`Search Completed, {results} results.`")
        else:
            print("No comments found in hot.")
            await ctx.send("`No comments found in hot.`")


    @commands.command(aliases=['post', 'search', 's', 'r'])
    async def check(self, ctx, sub, *,term):

        term = term.split(",")

        for item in term:
            # if item in config.preset_terms:
            try:
                [term.append(x) for x in config.preset_terms[item.lower()]]
            except:
                pass

        temp = []
        [temp.append(x.lower()) for x in term if x.lower() not in temp]

        term = temp

        results = 0
        try:
            subreddit = reddit.subreddit(sub)
        except:
            print(f"{sub} subreddit not found.")
            ctx.send(f"{sub} subreddit not found.")
        print("Searching...")
        await ctx.send("Searching...")
        sorting = subreddit.hot()
        found = False
        sep = '-'*50
        # term = term.lower()
        # term = term.split(",")
        await ctx.send(term)
        try:
            for submission in sorting:
                await asyncio.sleep(0)
                output = ''
                # for word in submission.title:
                for phrase in term:
                    if phrase in submission.title.lower():
                        found = True
                        output += f'\n{sep}\n'
                        output += ("""Title: {}
                            \nUpvotes: {}
                            \nhttps://www.reddit.com{}""".format(submission.title, submission.ups, submission.permalink))
                        output += f'\n{sep}\n'
                        await ctx.send(output)
                        results += 1
                        break
            if found:
                print(f"Search Completed, {results} result(s).")
                await ctx.send(f"`Search Completed, {results} result(s).`")
            else:
                print("No posts found in hot.")
                await ctx.send("`No posts found in hot.`")
        except:
            await ctx.send("Not a valid subreddit.")

def setup(client):
    client.add_cog(CheckReddit(client))
