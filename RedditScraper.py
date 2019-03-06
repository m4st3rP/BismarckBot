import praw
import asyncio


class RedditScraper:
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.reddit = praw.Reddit("bot1")
        self.subreddit = self.reddit.subreddit(subreddit_name)
        self.donePosts = []

    async def get_posts(self, min_score):
        links = []
        for submission in self.subreddit.hot(limit=25):
            await asyncio.sleep(2)
            if submission.score >= min_score:
                post_url = submission.url
                if post_url not in self.donePosts:
                    links.append(post_url)
                    self.donePosts.append(post_url)

        return links
