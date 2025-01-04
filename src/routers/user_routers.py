import base64

from flask import request, render_template, redirect, flash, session, jsonify, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from src import app, db, yandex
from src.models import User, InventoryItem, Aplications, log_to_db, ReturnAplication
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv
import requests, os

load_dotenv()

@app.route('/', methods=['GET'])
@login_required
def main():
    log_to_db(f"{current_user.username} зашел на главную страницу.")
    return render_template("index.html", username=current_user.username)


@app.route('/my_inventory', methods=['GET', 'POST'])
@login_required
def my_inventory():
    applet = []
    try:
        id = current_user.id
        good_applications = Aplications.query.filter_by(user_id=id).all()
        applet = [app for app in good_applications if app.status == "accepted"]
        log_to_db(f"Пользователь {current_user.username} просмотрел свой инвентарь.")

        if request.method == 'POST':
            applet_id = request.form.get('app_id')
            if applet_id is not None:
                try:
                    applet_id = int(applet_id)
                    if applet_id in [i.id for i in applet]:
                        This_applet = Aplications.query.filter_by(id=applet_id).first()
                        ReturnApplet = ReturnAplication(
                            user_id=This_applet.user_id,
                            item_id=This_applet.item_id,
                            status=This_applet.status,
                            quantity=This_applet.count,
                            username=This_applet.name,
                            item_name=InventoryItem.query.filter_by(id=This_applet.item_id).first().name,
                        )
                        db.session.add(ReturnApplet)
                        db.session.commit()
                        flash("Ваша заявка принята и будет рассмотрена администратором", 'success')
                    else:
                        flash('Некорректный запрос', 'error')
                except ValueError:
                    flash('Некорректный ID заявки', 'error')
            else:
                flash('ID заявки не указан', 'error')

    except Exception as e:
        log_to_db(f"Ошибка при получении инвентаря для пользователя {current_user.username}: {e}")

    return render_template("my_inventory.html", username=current_user.username, aplications=applet, items=InventoryItem.query.all())


@app.route('/return_item/<int:app_id>', methods=['GET', 'POST'])
@login_required
def return_item(app_id):
    applets = Aplications.query.filter_by(id=app_id).all()
    if applets:
        applets[0].status = "return"
        item = InventoryItem.query.filter_by(id=applets[0].item_id).first()
        item.quantity += applets[0].count
        db.session.commit()
        log_to_db(f"{current_user.username} вернул инвентарный элемент {app_id}")
        flash(f'Вы вернули {applets[0].count} элемента {item.name}', 'success')
    else:
        log_to_db(f"Попытка вернуть инвентарный элемент не удалась: ID {app_id} не найден")
        flash('Запись не найдена', 'error')
    return redirect('/my_inventory')


@app.route('/account', methods=['GET'])
@login_required
def account():
    try:
        applet = Aplications.query.filter_by(user_id=current_user.id).all()
        log_to_db(f"Пользователь {current_user.username} просмотрел свои заявки.")
    except Exception as e:
        applet = []
        log_to_db(f"Ошибка при получении заявок для пользователя {current_user.username}: {e}")
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
                if 0 < count_int <= item.quantity:
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
                    log_to_db(f"Пользователь {current_user.username} добавил заявку на элемент ID {id} с количеством {count_int}.")
                else:
                    flash("Ошибка количества инвентаря", category='error')
                    log_to_db(f"Пользователь {current_user.username} попытался добавить заявку с недопустимым количеством: {count}.")
            except ValueError:
                flash("Некорректное значение для количества", category='error')
                log_to_db(f"Пользователь {current_user.username} ввел некорректное значение для количества: {count}.")
            except Exception as e:
                log_to_db(f"Ошибка при добавлении заявки пользователем {current_user.username}: {e}")
        else:
            flash("ID элемента не найден", category='error')
            log_to_db(f"Пользователь {current_user.username} попытался добавить заявку с несуществующим ID элемента: {id}.")
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
            log_to_db(f"Попытка регистрации пользователем {username}: пароли не совпадают.")
        elif "@" not in email:
            flash('Неверный адрес почты', category='error')
            log_to_db(f"Попытка регистрации пользователем {username}: неверный адрес электронной почты.")
        else:
            pass_hash = generate_password_hash(password)
            new_user = User(username=username, password=pass_hash, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация прошла успешно! Вы можете войти.', category='success')
                log_to_db(f"Пользователь {username} зарегистрировался успешно.")
                return redirect("/login")
            except IntegrityError:
                db.session.rollback()
                flash("Имя пользователя уже занято", category='error')
                log_to_db(f"Попытка регистрации пользователем {username}: имя пользователя уже занято.")
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
            log_to_db(f"Пользователь {username} вошел в систему.")
            return redirect('/')
        else:
            flash('Некорректные данные', category='error')
            log_to_db(f"Попытка входа для пользователя {username}: некорректные данные.")
    return render_template('login_page.html')




@app.route('/yandex_login')
def yandex_login():
    redirect_uri = url_for('yandex_callback', _external=True)
    return yandex.authorize_redirect(redirect_uri, force_confirm=True)

@app.route('/yandex_callback')
def yandex_callback():
    token = yandex.authorize_access_token()
    user_info = get_user_info('yandex', token)
    return handle_oauth_callback(user_info, 'yandex', token)

def handle_oauth_callback(user_info, provider_name, token):
    if not user_info:
        flash(f'Ошибка получения информации о пользователе {provider_name}', 'error')
        return redirect(url_for('login'))

    email = user_info.get('default_email')
    if not email:
        flash(f'Не удалось получить email пользователя от {provider_name}. Пожалуйста попробуйте позже.', 'error')
        return redirect(url_for('login'))

    name = user_info.get('login')
    if not name:
        name = f"user_{user_info.get('id', 'unknown')}"
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        flash(f'Вы успешно вошли через {provider_name}!', 'success')
        user.yandex_access_token = token['access_token']
        db.session.commit()
        return redirect(url_for('main'))
    else:
        new_user = User(
            username=name,
            email=email,
            password='None',
            yandex_access_token=token['access_token']
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Вы успешно авторизовались через {provider_name}!', 'success')
        return redirect(url_for('main'))


def get_user_info(provider, token):
    if provider == 'yandex':
       resp = yandex.get('info', token=token)
       if resp.ok:
            return resp.json()
       else:
            return None
    else:
        return None

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    username = current_user.username
    token = current_user.yandex_access_token
    if token:
         try:
             data = {
                 'access_token': token,
                 'client_id': os.environ.get('YANDEX_CLIENT_ID'),
                 'client_secret': os.environ.get('YANDEX_CLIENT_SECRET')
             }
             response = requests.post('https://oauth.yandex.ru/revoke_token', data=data)
             current_user.yandex_access_token = None
             db.session.commit()
             log_to_db(f"Yandex токен успешно отозван для пользователя {username}.")
         except requests.exceptions.RequestException as e:
              log_to_db(f"Ошибка при отзыве токена Yandex для пользователя {username}: {e}")
              flash("Произошла ошибка при выходе из Yandex", 'error')
    logout_user()
    session.clear()
    log_to_db(f"Пользователь {username} вышел из системы.")
    return redirect('/login')