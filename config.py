from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    # Base Config
    DEBUG=True
    # DB Config
    DB_PORT=3306


class DevConfig(Config):
    DEBUG=True
    DB_IP="localhost"

class PrdConfig(Config):
    DEBUG=False
    DB_IP="0.0.0.0"    