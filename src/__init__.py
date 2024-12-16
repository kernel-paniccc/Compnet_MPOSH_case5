from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import base64

app = Flask(__name__)
app.secret_key = base64.b64encode('SUPER_KEY'.encode()).decode()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
manager = LoginManager(app)

from src import models, routers

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

