#This is only a test for now. Support for Reddit and Youtube videos is planned in the future

import praw
from dotenv import load_dotenv
import os

load_dotenv('../.env.local')

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

post = reddit.submission(url='')
print(post.score)
