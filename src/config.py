from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    # Base Config
    DEBUG=True

    # DB Config
    DB = {
        "user": "",
        "password": "", # 암호화 필요
        "host": "",
        "port": "30002",
        "database": "pikatwo",
    }

    @property
    def DB_URI(self):
        return f"mysql+mysqlconnector://{self.DB['user']}:{self.DB['password']}@{self.DB['host']}:{self.DB['port']}/{self.DB['database']}"
    
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG=True
    DB = {
        "user": "root",
        "password": "passw0rd", # 암호화 필요
        "host": "169.56.100.104",
        "port": "30002",
        "database": "pikatwo",
    }

class PrdConfig(Config):
    DEBUG=False
    DB = {
        "user": environ.get("DB_USER") if environ.get("DB_USER") != "" else "",
        "password": environ.get("DB_PASSWORD") if environ.get("DB_PASSWORD") != "" else "", # 암호화 필요
        "host": environ.get("DB_HOST") if environ.get("DB_USER") != "" else "",
        "port": "30002",
        "database": "pikatwo",
    }