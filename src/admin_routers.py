from flask import request, render_template, redirect, flash, send_file
from flask_login import login_required
from src import app, db
from src.models import InventoryItem, Aplications, admin_required
import logging

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')


@app.route('/admin/get_user_applet', methods=['GET', 'POST'])
@login_required
@admin_required
def get_user_applet():
    applet = Aplications.query.all()
    return render_template('get_user_applet.html', applets=applet)


@app.route('/admin/inventory_add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_inventory_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        status = request.form['status']
        new_item = InventoryItem(name=name, quantity=quantity, status=status)
        db.session.add(new_item)
        db.session.commit()
        logging.info(f"Добавлен инвентарный элемент: {name}, количество: {quantity}, статус: {status}")
        flash("Инвентарь добавлен", category='success')
    return render_template('add_inventory_item.html')


@app.route('/admin/all_item', methods=['GET', 'POST'])
@login_required
@admin_required
def all_inventory_item():
    items = InventoryItem.query.all()
    return render_template('all_items.html', items=items)


@app.route('/admin/del_applet/<int:applet_id>')
@login_required
@admin_required
def delited_applet(applet_id):
    item = Aplications.query.get(applet_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        logging.info(f"Запись приложения удалена: ID {applet_id}")
        flash('Запись удалена', 'success')
    else:
        logging.warning(f"Попытка удалить запись приложения не удалась: ID {applet_id} не найден")
        flash('Запись не найдена', 'error')
    return redirect('/admin/get_user_applet')


import logging
from flask import render_template, request, redirect, flash
from flask_login import login_required
from src.models import Aplications, InventoryItem, admin_required
from src import db


@app.route('/admin/edit_applet_status/<int:applet_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_applet(applet_id):
    applet = Aplications.query.get(applet_id)
    if not applet:
        logging.warning(f"Попытка редактирования статуса приложения не удалась: ID {applet_id} не найден")
        flash('Приложение не найдено', 'error')
        return redirect('/admin/all_applet')
    if request.method == 'POST':
        new_status = request.form['status']
        if applet.status != new_status:
            item = InventoryItem.query.get(applet.item_id)
            if new_status == 'not accepted':
                if item:
                    item.quantity += applet.count
                    logging.info(f"Количество для {item.name} увеличено на {applet.count}")
                    flash(f'Количество для {item.name} увеличено на {applet.count}', 'success')
                applet.status = new_status
            elif new_status == 'accepted':
                if item:
                    if item.quantity >= applet.count:
                        item.quantity -= applet.count
                        logging.info(f"Количество для {item.name} уменьшено на {applet.count}")
                        flash(f'Количество для {item.name} уменьшено на {applet.count}', 'success')
                        applet.status = new_status
                    else:
                        flash(f'Недостаточно количества для {item.name}', 'error')
                        logging.warning(
                            f"Не удалось изменить статус приложения ID {applet_id}: недостаточно количества для {item.name}")
                        return redirect('/admin/get_user_applet')
                else:
                    flash('Товар не найден в инвентаре', 'error')
                    logging.warning(f"Не удалось изменить статус приложения ID {applet_id}: товар не найден")
            db.session.commit()
            logging.info(f"Статус приложения изменен: ID {applet_id}, новый статус: {new_status}")
    return redirect('/admin/get_user_applet')


@app.route('/admin/del/<int:item_id>')
@login_required
@admin_required
def delited(item_id):
    item = InventoryItem.query.get(item_id)
    applets = Aplications.query.filter_by(item_id=item_id).all()
    if item:
        for applet in applets:
            db.session.delete(applet)
        db.session.delete(item)
        db.session.commit()
        logging.info(f"Запись инвентарного элемента удалена: ID {item_id}")
        flash('Запись удалена', 'success')
    else:
        logging.warning(f"Попытка удалить инвентарный элемент не удалась: ID {item_id} не найден")
        flash('Запись не найдена', 'error')
    return redirect('/admin/all_item')

@app.route('/admin/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    item = InventoryItem.query.get(item_id)
    if not item:
        logging.warning(f"Попытка редактирования инвентарного элемента не удалась: ID {item_id} не найден")
        return redirect('/admin')

    if request.method == 'POST':
        old_name = item.name
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.status = request.form['status']
        db.session.commit()
        logging.info(
            f"Данные инвентарного элемента изменены: ID {item_id}, старое имя: {old_name}, новое имя: {item.name}")

    return redirect('/admin/all_item')

@app.route('/admin/get_logs')
@login_required
@admin_required
def get_logs():
    return send_file('logs/app.log', as_attachment=True)

