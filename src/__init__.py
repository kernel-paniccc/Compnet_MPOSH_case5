from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import logging, base64, os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("src/logs/app.log"),
                        logging.StreamHandler()
                    ])
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
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

from src import models, user_routers, buy_routers, admin_routers

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()
