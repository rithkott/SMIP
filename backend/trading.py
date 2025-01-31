import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from models import db, TradeModel
import tiktok_algo

def make_trade(args):
    try:
        likes_current, followers_current = asyncio.run(tiktok_algo.get_likes_and_followers(args['video_link']))
        trade = TradeModel(
            user_id=args['user_id'],
            initial_amount=args['initial_amount'],
            ongoing=True,
            datetime_started=datetime.now(ZoneInfo('UTC')),
            likes_initial=likes_current,
            followers=followers_current,
            video_link=args['video_link']
        )
        db.session.add(trade)
        db.session.commit()
    except Exception as e:
        print(f"Error creating trade: {e}")

def update_trade(trade):
    try:
        trade.ongoing = False
        trade.likes_final = asyncio.run(tiktok_algo.get_likes(trade.video_link))
        trade.multiplier = tiktok_algo.reward_algo_net(trade.likes_initial, trade.likes_final, trade.followers)
        trade.final_amount = trade.initial_amount + (trade.initial_amount * trade.multiplier)
        trade.datetime_ended = datetime.now(ZoneInfo('UTC'))
        db.session.commit()
    except Exception as e:
        print(f"Error updating trade: {e}")