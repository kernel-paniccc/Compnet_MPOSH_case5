from flask import request, render_template, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from src import app, db
from src.models import User, InventoryItem, Aplications
from sqlalchemy.exc import IntegrityError
import logging


@app.route('/', methods=['GET'])
@login_required
def main():
    logging.info(f"{current_user.username} зашел на главную страницу.")
    return render_template("index.html", username=current_user.username)

@app.route('/account', methods=['GET'])
@login_required
def account():
    try:
        applet = Aplications.query.filter_by(user_id=current_user.id).all()
        logging.info(f"Пользователь {current_user.username} просмотрел свои заявки.")
    except Exception as e:
        applet = []
        logging.error(f"Ошибка при получении заявок для пользователя {current_user.username}: {e}")
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
                    logging.info(f"Пользователь {current_user.username} добавил заявку на элемент ID {id} с количеством {count_int}.")
                else:
                    flash("Слишком большое значение", category='error')
                    logging.warning(f"Пользователь {current_user.username} попытался добавить заявку с недопустимым количеством: {count}.")
            except ValueError:
                flash("Некорректное значение для количества", category='error')
                logging.error(f"Пользователь {current_user.username} ввел некорректное значение для количества: {count}.")
            except Exception as e:
                logging.error(f"Ошибка при добавлении заявки пользователем {current_user.username}: {e}")
        else:
            flash("ID элемента не найден", category='error')
            logging.warning(f"Пользователь {current_user.username} попытался добавить заявку с несуществующим ID элемента: {id}.")
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
            logging.warning(f"Попытка регистрации пользователем {username}: пароли не совпадают.")
        elif "@" not in email:
            flash('Неверный адрес почты', category='error')
            logging.warning(f"Попытка регистрации пользователем {username}: неверный адрес электронной почты.")
        else:
            pass_hash = generate_password_hash(password)
            new_user = User(username=username, password=pass_hash, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация прошла успешно! Вы можете войти.', category='success')
                logging.info(f"Пользователь {username} зарегистрировался успешно.")
                return redirect("/login")
            except IntegrityError:
                db.session.rollback()
                flash("Имя пользователя уже занято", category='error')
                logging.warning(f"Попытка регистрации пользователем {username}: имя пользователя уже занято.")
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
            logging.info(f"Пользователь {username} вошел в систему.")
            return redirect('/')
        else:
            flash('Некорректные данные', category='error')
            logging.warning(f"Попытка входа для пользователя {username}: некорректные данные.")
    return render_template('login_page.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    username = current_user.username
    logout_user()
    logging.info(f"Пользователь {username} вышел из системы.")
    return redirect('/login')
