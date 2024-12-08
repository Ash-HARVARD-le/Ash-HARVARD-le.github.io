from . import db
from flask_login import UserMixin

# User database, stores their login information, cash, and personal sensitive info
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(512))
    cash = db.Column(db.Float, default=100.0)
    huid = db.Column(db.String(8), unique=True, nullable=True)
    huid_locked = db.Column(db.Boolean, default=False)

    # Links a user to these other databases
    deposits = db.relationship('Deposit', backref='user', lazy=True)
    game_stats = db.relationship('GameStats', backref='user', lazy=True)

# Keep track of any deposit information (in the real world this would be valid)
class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    deposit_type = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(16), nullable=True)
    exp_date = db.Column(db.String(5), nullable=True)
    cvv = db.Column(db.String(4), nullable=True)

# Database for ALL GAMES PLAYED: stores user, the game type, bet and result
class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    game_type = db.Column(db.String(10), nullable=False)
    bet = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(5), nullable=False)