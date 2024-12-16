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
        print([i.id for i in applet])
    except Exception as e:
        applet = []
    return render_template("account.html", username=current_user.username, applications=applet)


@app.route('/applications', methods=['GET', 'POST'])
@login_required
def main_application():
    items = InventoryItem.query.filter_by(user_id=0).all()

    if request.method == 'POST':
        id = request.form.get('item_id')
        item = InventoryItem.query.filter_by(id=id).all()
        if id and item:
            status = "not accepted"
            new_application = Aplications(user_id=current_user.id, name=current_user.username, item_id=id, status=status)
            try:
                db.session.add(new_application)
                db.session.commit()
                flash("Заявка добавлена", category='success')
            except Exception as e:
                flash("ID элемента не найден", category='error')
        else:
            flash("ID элемента не найден", category='error')
    return render_template('applications.html', items=items)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin():
        return redirect('/')
    return render_template('admin.html')


@app.route('/admin/inventory_add', methods=['GET', 'POST'])
@login_required
def add_inventory_item():
    if not current_user.is_admin():
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        status = request.form['status']
        new_item = InventoryItem(name=name, quantity=quantity, status=status)
        db.session.add(new_item)
        db.session.commit()
        flash("Инвентарь добавлен", category='success')
    return render_template('add_inventory_item.html')


@app.route('/admin/all_item', methods=['GET', 'POST'])
@login_required
def all_inventory_item():
    if not current_user.is_admin():
        return redirect('/')
    items = InventoryItem.query.all()

    return render_template('all_items.html', items=items)


@app.route('/del/<int:item_id>')
@login_required
def delited(item_id):
    if not current_user.is_admin():
        return redirect('/')
    item = InventoryItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Запись удалена', 'success')
    else:
        flash('Запись не найдена', 'error')
    return redirect('/admin/all_item')


@app.route('/admin/edit/<int:item_edit_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_edit_id):
    if not current_user.is_admin():
        return redirect('/')
    item = InventoryItem.query.get(item_edit_id)
    if not item: return redirect('/admin')
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.status = request.form['status']
        db.session.commit()
        flash('Данные изменены', 'success')
        return redirect('/admin/all_item')
    return render_template('edit_item.html', item=item)


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
