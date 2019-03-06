import praw
import discord
import asyncio


class BismarckBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.channel_id = open("channel.txt", "r").readline()
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.post_subreddit_images("animemes", 3000, self.channel_id))
        self.done_posts = []
        self.token = open("token.txt", "r").readline()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        with open("done_posts.txt", "r") as f:
            for line in f:
                self.done_posts.append(line.strip())

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!hallo'):
            await message.channel.send('Hallo!')

    async def post_subreddit_images(self, subreddit_name, min_score, channel_id):
        await self.wait_until_ready()
        channel = self.get_channel(channel_id)  # channel ID goes here
        while not self.is_closed():
            posts = await self.get_posts(subreddit_name, min_score)
            for post in posts:
                await channel.send(post)
                await asyncio.sleep(3)
            await asyncio.sleep(1800)  # task runs every 30 min

    async def get_posts(self, subreddit_name, min_score):
        reddit = praw.Reddit("bot1")
        subreddit = reddit.subreddit(subreddit_name)

        links = []
        for submission in subreddit.hot(limit=25):
            await asyncio.sleep(2)
            if submission.score >= min_score:
                post_url = submission.url
                if post_url not in self.done_posts:
                    links.append(post_url)
                    self.done_posts.append(post_url)
                    with open("done_posts.txt", "a") as f:
                        f.write(post_url + "\n")
        return links


client = BismarckBot()
client.run(client.token)
