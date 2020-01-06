import praw, os

reddit = praw.Reddit(client_id=os.getenv("redditID"),
                     client_secret=os.getenv('redditSecret'),
                     username=os.getenv('redditUsername'),
                     password=os.getenv('redditPass'),
                     user_agent="RedditWatcher")

def livecheck():
    terms = os.getenv("terms")
    subreddit = reddit.subreddit('all')
    context = 3
    for comment in subreddit.stream.comments():
        output = ''
        for word in comment.body.split():
            if word.lower() in terms:
                try:
                    # print(30*"-")
                    output += 'Comment:'
                    output += comment.body
                    output += 'https://www.reddit.com'
                    output += comment.permalink 
                    output += "?context=" 
                    output += str(context)
                    # print(30*"-")
                    print(output)
                    dm(os.getenv.author, output)
                    break

                except praw.exceptions.PRAWException:
                    pass
