import praw
from dotenv import load_dotenv
import os

load_dotenv('../.env.local')

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

post = reddit.submission(url='https://www.reddit.com/r/What/comments/1i2ioik/what_is_the_reasoning_for_doing_this/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button')
print(post.score)
