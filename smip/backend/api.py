from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import tiktok_algo
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model): 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    credits = db.Column(db.Integer, unique=False, nullable=False, default=0)
    def __repr__(self): 
        return f"User(username = {self.username}, email = {self.email}, credits = {self.credits})"

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'username':fields.String,
    'email':fields.String,
    'credits':fields.Integer
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args["username"], email=args["email"])
        db.session.add(user)
        try: 
            db.session.commit()
            users = UserModel.query.all()
            return users, 201
        except Exception:
            db.session.rollback()
            abort(400, message="User already exists")
        
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, email):
        user = UserModel.query.filter_by(email=email).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
    @marshal_with(userFields)
    def patch(self, email):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(email=email).first() 
        if not user: 
            abort(404, message="User not found")
        user.username = args["username"]
        user.email = args["email"]
        user.credits = args["credits"]
        db.session.commit()
        return user 
    
    @marshal_with(userFields)
    def delete(self, email):
        user = UserModel.query.filter_by(email=email).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


#Trades Classes

class TradeModel(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True)
    ongoing = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    initial_amount = db.Column(db.Integer, nullable=False)
    final_amount = db.Column(db.Integer, nullable=True)
    datetime_started = db.Column(db.String(30), nullable=False)
    datetime_ended = db.Column(db.String(30), nullable=True)
    likes_initial = db.Column(db.Integer, nullable=False)
    likes_final = db.Column(db.Integer, nullable=True)
    followers = db.Column(db.Integer, nullable=True)
    multiplier = db.Column(db.Float, nullable=True)
    video_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        tradestring = '''
            Trade(
                trade_id = {self.trade_id}
                ongoing = {self.ongoing}
                user_id = {self.user_id}
                intial_amount = {self.initial_amount}
                final_amount = {self.final_amount}
                datetime_started = {self.datetime_started}
                datetime_ended = {self.datetime_ended}
                likes_initial = {self.likes_initial}
                likes_final = {self.likes_final}
                followers = {self.followers}
                multiplier = {self.multiplier}
                video_link = {self.video_link}
                )
        '''
        return tradestring

trade_args = reqparse.RequestParser()
trade_args.add_argument('user_id', type=int, required=True, help="User ID Required")
trade_args.add_argument('initial_amount', type=int, required=True, help="Amount Required")
trade_args.add_argument('video_link', type=str, required=True, help="Video Link Required")

tradeFields = {
    'trade_id': fields.Integer,
    'user_id': fields.Integer,
    'ongoing': fields.Boolean,
    'initial_amount': fields.Integer,
    'final_amount': fields.Integer,
    'datetime_started': fields.String,
    'datetime_ended': fields.String,
    'likes_initial': fields.Integer,
    'likes_final': fields.Integer,
    'followers': fields.Integer,
    'multiplier': fields.Float,
    'video_link': fields.String
}

class Trade(Resource):
    @marshal_with(tradeFields)
    def get(self, trade_id):
        trade = TradeModel.query.filter_by(trade_id=trade_id).first()
        if not trade:
            abort(404, message="Trade not found")
        return trade

    @marshal_with(tradeFields)
    def patch(self, trade_id):
        trade = TradeModel.query.filter_by(trade_id=trade_id).first()
        if not trade:
            abort(404, message="Trade not found")
        
        # Update the trade fields
        trade.ongoing=False
        trade.datetime_ended = datetime.now(ZoneInfo('UTC'))
        trade.likes_final = asyncio.run(tiktok_algo.get_likes(trade.video_link))
        trade.multiplier = tiktok_algo.reward_algo_net(trade.likes_initial, trade.likes_final, trade.followers)
        trade.final_amount = trade.initial_amount + (trade.initial_amount * trade.multiplier)

        db.session.commit()
        return trade

    @marshal_with(tradeFields)
    def delete(self, trade_id):
        trade = TradeModel.query.filter_by(trade_id=trade_id).first()
        if not trade:
            abort(404, message="Trade not found")
        db.session.delete(trade)
        db.session.commit()
        return {}, 204

class Trades(Resource):
    @marshal_with(tradeFields)
    def get(self):
        trades = TradeModel.query.all()  # Retrieves all trades
        return trades

    @marshal_with(tradeFields)
    def post(self):
        args = trade_args.parse_args()  # Parse the input arguments
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
        return trade, 201
    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<string:email>')
api.add_resource(Trades, '/api/trades/')
api.add_resource(Trade, '/api/trades/<int:trade_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 