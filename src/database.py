from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import DevConfig

db = SQLAlchemy()
migrate = Migrate()
