from functools import wraps

from flask import flash, redirect
from flask_login import UserMixin, current_user
from src import db, manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')

    def __repr__(self):
        return f'<User {self.username} (ID: {self.id}, Role: {self.role})>'

    def is_admin(self):
        return self.role == 'admin'

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'new', 'used', 'broken'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    user = db.relationship('User', backref='inventory_items')

    def __repr__(self):
        return f'<InventoryItem {self.name} (Quantity: {self.quantity}, Status: {self.status})>'

class Aplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, default=0)


    def __repr__(self):
        return f'<InventoryItem {self.name} (Quantity: {self.quantity}, Status: {self.status})>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(100), nullable=False)

# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.is_admin()
#
# admin = Admin(app, name='My Admin', template_mode='bootstrap3')
# admin.add_view(MyModelView(InventoryItem, db.session))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
