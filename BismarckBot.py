import discord
import asyncio
from RedditScraper import RedditScraper


class BismarckBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rs = RedditScraper("animemes")
        self.channel_id = open("channel.txt", "r").readline()
        self.token = open("token.txt", "r").readline()
        self.bg_task = self.loop.create_task(self.post_subreddit_images())  # create the background task and run it in the background

    async def post_subreddit_images(self):
        await self.wait_until_ready()
        channel = self.get_channel(self.channel_id)
        while not self.is_closed:
            print("Ich hol mir mal paar Bilder")
            posts = await self.rs.get_posts(3000)
            print("Bilder geholt")
            for post in posts:
                await channel.send(post)
                print("Ein Bild gepostet")
                await asyncio.sleep(3)
            print("Fertig mit Bilder posten")
            await asyncio.sleep(1800)  # task runs every 30 minutes

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!hallo'):
            await message.channel.send('Hallo!')


client = BismarckBot()
client.run(client.token)
