from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

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
