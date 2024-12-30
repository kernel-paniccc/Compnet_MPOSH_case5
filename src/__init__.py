from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import base64, os

from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)

app.secret_key = base64.b64encode(str(os.getenv("KEY")).encode()).decode()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

manager = LoginManager(app)
manager.init_app(app)
manager.login_view = 'login'

migrate = Migrate(app, db)

from src import models
from src.routers import admin_routers, buy_routers, user_routers, log_routers
from src.models import User

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = generate_password_hash(os.getenv("ADMIN_PASS"))
    admin_email = os.getenv("ADMIN_EMAIL")


    admin=User(
        username=admin_username,
        password=admin_password,
        email=admin_email,
        role="admin"
    )
    db.create_all()

    existing_admin = User.query.filter_by(username=admin_username).first()
    if existing_admin is None:
        db.session.add(admin)
        db.session.commit()
