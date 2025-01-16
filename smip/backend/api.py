from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

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

    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<string:email>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 