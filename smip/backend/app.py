from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from datetime import datetime
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)


#Users Classes

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self): 
        return f"User(name = {self.username}, email = {self.email}, credits={self.credits})"

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'username':fields.String,
    'email':fields.String,
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
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        user.username = args["username"]
        user.email = args["email"]
        db.session.commit()
        return user 
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


#Trades Classes

class TradeModel(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    datetime_started = db.Column(db.String(30), nullable=False)
    datetime_ended = db.Column(db.String(30), nullable=True)
    likes_inital = db.Column(db.Integer, nullable=False)
    likes_final = db.Column(db.Integer, nullable=True)
    video_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        tradestring = '''
            Trade(
                trade_id = {self.trade_id}
                user_id = {self.user_id}
                amount = {self.amount}
                datetime_started = {self.datetime_started}
                datetime_ended = {self.datetime_ended}
                likes_inital = {self.likes_inital}
                likes_final = {self.likes_final}
                video_link = {self.video_link}
                )
        '''
        return tradestring

trade_args = reqparse.RequestParser()
trade_args.add_argument('user_id', type=int, required=True, help="User ID Required")
trade_args.add_argument('amount', type=int, required=True, help="Amount Required")
trade_args.add_argument('datetime_started', type=str, required=True, help="Datetime Started Required")
trade_args.add_argument('datetime_ended', type=str, required=False)
trade_args.add_argument('likes_initial', type=int, required=True, help="Initial Likes Required")
trade_args.add_argument('likes_final', type=int, required=False)
trade_args.add_argument('video_link', type=str, required=True, help="Video Link Required")

tradeFields = {
    'trade_id': fields.Integer,
    'user_id': fields.Integer,
    'amount': fields.Integer,
    'datetime_started': fields.String,
    'datetime_ended': fields.String,
    'likes_inital': fields.Integer,
    'likes_final': fields.Integer,
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
        args = trade_args.parse_args()
        trade = TradeModel.query.filter_by(trade_id=trade_id).first()
        if not trade:
            abort(404, message="Trade not found")
        
        # Update the trade fields
        trade.user_id = args['user_id']
        trade.amount = args['amount']
        trade.datetime_started = args['datetime_started']
        trade.datetime_ended = args['datetime_ended']
        trade.likes_inital = args['likes_initial']
        trade.likes_final = args['likes_final']
        trade.video_link = args['video_link']

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
        trade = TradeModel(
            user_id=args['user_id'],
            amount=args['amount'],
            datetime_started=args['datetime_started'],
            datetime_ended=args.get('datetime_ended'),
            likes_inital=args['likes_initial'],
            likes_final=args.get('likes_final'),
            video_link=args['video_link']
        )
        db.session.add(trade)
        db.session.commit()
        return trade, 201



#Registering
    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Trades, '/api/trades/')
api.add_resource(Trade, '/api/trades/<int:trade_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 