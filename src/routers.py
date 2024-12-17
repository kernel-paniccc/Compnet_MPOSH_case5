from flask import request, render_template, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from src import app, db
from src.models import User, InventoryItem, Aplications
from sqlalchemy.exc import IntegrityError


@app.route('/', methods=['GET'])
@login_required
def main():
    return render_template("index.html", username=current_user.username)


@app.route('/account', methods=['GET'])
@login_required
def account():
    try:
        applet = Aplications.query.filter_by(user_id=current_user.id).all()
    except Exception as e:
        applet = []
    return render_template("account.html", username=current_user.username, applications=applet)


@app.route('/applications', methods=['GET', 'POST'])
@login_required
def main_application():
    items = InventoryItem.query.filter_by(user_id=0).all()
    if request.method == 'POST':
        id = request.form.get('item_id')
        count = request.form.get('value')
        item = InventoryItem.query.filter_by(id=id).first()
        if id and item:
            try:
                count_int = int(count)
                if 0 < count_int < item.quantity:
                    status = "not accepted"
                    new_application = Aplications(
                        user_id=current_user.id,
                        name=current_user.username,
                        item_id=id,
                        status=status,
                        count=count_int
                    )
                    db.session.add(new_application)
                    db.session.commit()
                    flash("Заявка добавлена", category='success')
                else:
                    flash("Слишком большое значение", category='error')
            except ValueError:
                flash("Некорректное значение для количества", category='error')
            except Exception as e:
                print(e)
        else:
            flash("ID элемента не найден", category='error')

    return render_template('applications.html', items=items)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    session.clear()
    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_return = request.form['password_return']

        if password != password_return:
            flash('Пароли не совпадают', category='error')
        elif "@" not in email:
            flash('Неверный адрес почты', category='error')
        else:
            pass_hash = generate_password_hash(password)
            new_user = User(username=username, password=pass_hash, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация прошла успешно! Вы можете войти.', category='success')
                return redirect("/login")
            except IntegrityError:
                db.session.rollback()
                flash("Имя пользователя уже занято", category='error')
    return render_template("register_page.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if current_user.is_authenticated:
        logout_user()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли!', category='success')
            return redirect('/')
        else:
            flash('Некорректные данные', category='error')
    return render_template('login_page.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', category='info')
    return redirect('/login')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/login')
    return response
