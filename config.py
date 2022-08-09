from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    # Base Config
    DEBUG=True

    # DB Config
    DB = {
        "user": "root",
        "password": "", # 암호화 필요
        "host": "",
        "port": "3306",
        "database": "",
    }

    @property
    def DB_URI(self):
        return f"mysql+pymysql://{self.DB['user']}:{self.DB['password']}@{self.DB['host']}:{self.DB['port']}/{self.DB['database']}"
    
    SQLALCHEMY_DATABASE_URI = DB_URI

class DevConfig(Config):
    DEBUG=True
    DB = {
        "user": "root",
        "password": "", # 암호화 필요
        "host": "localhost",
        "port": "3306",
        "database": "development",
    }

class PrdConfig(Config):
    DEBUG=False
    DB = {
        "user": "root",
        "password": "", # 암호화 필요
        "host": "0.0.0.0",
        "port": "3306",
        "database": "production",
    }