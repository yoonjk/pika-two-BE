from flask import Flask
from os import environ

app = Flask(__name__)

if environ.get("FLASK_ENV") == "dev":
    app.config.from_object("config.DevConfig")
else:
    app.config.from_object("config.PrdConfig")

@app.route('/')
def hello():
    msg = "DB_IP={}, debug={}".format(app.config["DB_IP"], app.config["DEBUG"])
    return msg
    
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
    print(app.config["DB_IP"])