from flask import Flask
from src.database import db

class User(db.Model):
    __table_name__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    nickname = db.Column(db.String(256), unique=True, nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, )
    profession = db.Column(db.String(256), )    # 직무
    applied_posts = db.relationship()