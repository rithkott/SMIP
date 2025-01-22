from TikTokApi import TikTokApi
from dotenv import load_dotenv
import os
import asyncio
from pprint import pprint
import math

load_dotenv('../.env.local') # get your own ms_token from your cookies on tiktok.com

async def get_likes(url):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[os.getenv("TIKTOK_MSTOKEN")], num_sessions=1, sleep_after=3, browser='webkit')
        video = await api.video(url=url).info()
        return video.get('stats')['diggCount']

async def get_likes_and_followers(url):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[os.getenv("TIKTOK_MSTOKEN")], num_sessions=1, sleep_after=3, browser='webkit')
        video = await api.video(url=url).info()
        return (video.get('stats')['diggCount'], video.get('authorStats')['followerCount'])


# asyncio.run(get_likes('https://www.tiktok.com/@eze.see/video/7430255302215355690?is_from_webapp=1&sender_device=pc'))

log_base = 10

def reward_algo_net(likes_initial, likes_final, followers):
    payout = (math.log((likes_final**2)/(likes_initial*followers), log_base))
    return payout


likes_initial = 30000
likes_final = 50000
followers = 35000

print(reward_algo_net(likes_initial, likes_final, followers))



